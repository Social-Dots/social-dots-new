import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Check for Stripe environment variables
stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')
stripe_webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

print("Stripe Environment Variables Check")
print("-" * 30)

# Check if keys are set
print(f"STRIPE_PUBLIC_KEY: {'✓ Set' if stripe_public_key else '✗ Not set'}")
print(f"STRIPE_SECRET_KEY: {'✓ Set' if stripe_secret_key else '✗ Not set'}")
print(f"STRIPE_WEBHOOK_SECRET: {'✓ Set' if stripe_webhook_secret else '✗ Not set'}")

# Check key formats (without revealing full keys)
if stripe_public_key:
    print(f"Public key format: {'✓ Valid' if stripe_public_key.startswith('pk_') else '✗ Invalid (should start with pk_)'}")
    print(f"Public key preview: {stripe_public_key[:8]}...{stripe_public_key[-4:]}")

if stripe_secret_key:
    print(f"Secret key format: {'✓ Valid' if stripe_secret_key.startswith('sk_') else '✗ Invalid (should start with sk_)'}")
    print(f"Secret key preview: {stripe_secret_key[:8]}...{stripe_secret_key[-4:]}")

if stripe_webhook_secret:
    print(f"Webhook secret format: {'✓ Valid' if stripe_webhook_secret.startswith('whsec_') else '✗ Invalid (should start with whsec_)'}")
    print(f"Webhook secret preview: {stripe_webhook_secret[:8]}...{stripe_webhook_secret[-4:]}")

# Summary
all_keys_set = all([stripe_public_key, stripe_secret_key, stripe_webhook_secret])
print("\nSummary:")
if all_keys_set:
    print("✓ All Stripe environment variables are set")
else:
    print("✗ Some Stripe environment variables are missing")
    print("\nTo fix this issue:")
    print("1. Make sure you have set the environment variables in your Vercel project settings")
    print("2. For local development, create a .env file with the required variables")
    print("3. Redeploy your application after setting the variables")

sys.exit(0 if all_keys_set else 1)