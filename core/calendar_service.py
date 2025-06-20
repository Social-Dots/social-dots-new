import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import CalendarEvent

logger = logging.getLogger(__name__)


class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.client_id = settings.GOOGLE_CALENDAR_CLIENT_ID
        self.client_secret = settings.GOOGLE_CALENDAR_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_CALENDAR_REDIRECT_URI

    def get_authorization_url(self):
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.SCOPES
        )
        flow.redirect_uri = self.redirect_uri
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state

    def exchange_code_for_tokens(self, code, state):
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.SCOPES,
            state=state
        )
        flow.redirect_uri = self.redirect_uri
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    def build_service(self, credentials_dict):
        credentials = Credentials(
            token=credentials_dict['token'],
            refresh_token=credentials_dict.get('refresh_token'),
            token_uri=credentials_dict['token_uri'],
            client_id=credentials_dict['client_id'],
            client_secret=credentials_dict['client_secret'],
            scopes=credentials_dict['scopes']
        )
        
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        
        return build('calendar', 'v3', credentials=credentials)

    def get_busy_times(self, credentials_dict, start_date, end_date, calendar_id='primary'):
        try:
            service = self.build_service(credentials_dict)
            
            body = {
                "timeMin": start_date.isoformat(),
                "timeMax": end_date.isoformat(),
                "items": [{"id": calendar_id}]
            }
            
            result = service.freebusy().query(body=body).execute()
            busy_times = result.get('calendars', {}).get(calendar_id, {}).get('busy', [])
            
            return busy_times
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting busy times: {e}")
            raise

    def get_available_slots(self, credentials_dict, date, duration_minutes=60, business_hours=(9, 17)):
        try:
            start_of_day = datetime.combine(date, datetime.min.time().replace(hour=business_hours[0]))
            end_of_day = datetime.combine(date, datetime.min.time().replace(hour=business_hours[1]))
            
            start_of_day = timezone.make_aware(start_of_day)
            end_of_day = timezone.make_aware(end_of_day)
            
            busy_times = self.get_busy_times(credentials_dict, start_of_day, end_of_day)
            
            available_slots = []
            current_time = start_of_day
            slot_duration = timedelta(minutes=duration_minutes)
            
            while current_time + slot_duration <= end_of_day:
                slot_end = current_time + slot_duration
                
                is_available = True
                for busy_period in busy_times:
                    busy_start = datetime.fromisoformat(busy_period['start'].replace('Z', '+00:00'))
                    busy_end = datetime.fromisoformat(busy_period['end'].replace('Z', '+00:00'))
                    
                    if (current_time < busy_end and slot_end > busy_start):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append({
                        'start': current_time,
                        'end': slot_end
                    })
                
                current_time += timedelta(minutes=30)
            
            return available_slots
            
        except Exception as e:
            logger.error(f"Error getting available slots: {e}")
            raise

    def create_event(self, credentials_dict, event_data):
        try:
            service = self.build_service(credentials_dict)
            
            event = {
                'summary': event_data['title'],
                'description': event_data.get('description', ''),
                'start': {
                    'dateTime': event_data['start_time'].isoformat(),
                    'timeZone': 'America/Toronto',
                },
                'end': {
                    'dateTime': event_data['end_time'].isoformat(),
                    'timeZone': 'America/Toronto',
                },
                'attendees': []
            }
            
            if event_data.get('attendee_email'):
                event['attendees'].append({
                    'email': event_data['attendee_email'],
                    'displayName': event_data.get('attendee_name', '')
                })
            
            if event_data.get('send_notifications', True):
                event['sendNotifications'] = True
            
            result = service.events().insert(
                calendarId='primary',
                body=event,
                sendNotifications=event_data.get('send_notifications', True)
            ).execute()
            
            calendar_event = CalendarEvent.objects.create(
                title=event_data['title'],
                description=event_data.get('description', ''),
                start_time=event_data['start_time'],
                end_time=event_data['end_time'],
                attendee_name=event_data.get('attendee_name', ''),
                attendee_email=event_data.get('attendee_email', ''),
                attendee_phone=event_data.get('attendee_phone', ''),
                google_event_id=result['id'],
                is_confirmed=True
            )
            
            logger.info(f"Calendar event created: {result['id']}")
            return calendar_event
            
        except HttpError as e:
            logger.error(f"Google Calendar API error creating event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            raise

    def update_event(self, credentials_dict, event_id, event_data):
        try:
            service = self.build_service(credentials_dict)
            
            event = service.events().get(calendarId='primary', eventId=event_id).execute()
            
            if 'title' in event_data:
                event['summary'] = event_data['title']
            if 'description' in event_data:
                event['description'] = event_data['description']
            if 'start_time' in event_data:
                event['start']['dateTime'] = event_data['start_time'].isoformat()
            if 'end_time' in event_data:
                event['end']['dateTime'] = event_data['end_time'].isoformat()
            
            result = service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            logger.info(f"Calendar event updated: {event_id}")
            return result
            
        except HttpError as e:
            logger.error(f"Google Calendar API error updating event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating calendar event: {e}")
            raise

    def delete_event(self, credentials_dict, event_id):
        try:
            service = self.build_service(credentials_dict)
            
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            
            try:
                calendar_event = CalendarEvent.objects.get(google_event_id=event_id)
                calendar_event.delete()
            except CalendarEvent.DoesNotExist:
                pass
            
            logger.info(f"Calendar event deleted: {event_id}")
            return True
            
        except HttpError as e:
            logger.error(f"Google Calendar API error deleting event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error deleting calendar event: {e}")
            raise

    def get_upcoming_events(self, credentials_dict, max_results=10):
        try:
            service = self.build_service(credentials_dict)
            
            now = datetime.utcnow().isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except HttpError as e:
            logger.error(f"Google Calendar API error getting events: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            raise


def book_appointment(appointment_data, calendar_credentials):
    try:
        calendar_service = GoogleCalendarService()
        
        event_data = {
            'title': f"Consultation with {appointment_data['name']}",
            'description': f"""
Consultation appointment booked through SocialDots.ca

Client: {appointment_data['name']}
Email: {appointment_data['email']}
Phone: {appointment_data.get('phone', 'Not provided')}
Service Interest: {appointment_data.get('service', 'General consultation')}
Message: {appointment_data.get('message', 'No additional message')}
            """.strip(),
            'start_time': appointment_data['start_time'],
            'end_time': appointment_data['end_time'],
            'attendee_name': appointment_data['name'],
            'attendee_email': appointment_data['email'],
            'attendee_phone': appointment_data.get('phone', ''),
            'send_notifications': True
        }
        
        calendar_event = calendar_service.create_event(calendar_credentials, event_data)
        
        logger.info(f"Appointment booked for {appointment_data['name']} on {appointment_data['start_time']}")
        return calendar_event
        
    except Exception as e:
        logger.error(f"Failed to book appointment: {e}")
        raise