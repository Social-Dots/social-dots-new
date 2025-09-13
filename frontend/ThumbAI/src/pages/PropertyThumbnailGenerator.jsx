import React, { useState, useEffect } from "react";
import { ThumbnailRequest } from "@/api/entities";
import { UsageLimit } from "@/api/entities";
import { User } from "@/api/entities";
import { UploadFile } from "@/api/integrations";

import HeroSection from "../components/hero/HeroSection";
import ImageUploader from "../components/upload/ImageUploader";
import ThumbnailResults from "../components/results/ThumbnailResults";
import NextSteps from "../components/next-steps/NextSteps";
import UsageLimitWarning from "../components/usage/UsageLimitWarning";

export default function PropertyThumbnailGenerator() {
    const [isProcessing, setIsProcessing] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [user, setUser] = useState(null);
    const [usageCount, setUsageCount] = useState(0);
    const [isLimitReached, setIsLimitReached] = useState(false);

    const DAILY_LIMIT = 3;

    useEffect(() => {
        checkUserAndUsage();
    }, []);

    const checkUserAndUsage = async () => {
        try {
            const currentUser = await User.me();
            setUser(currentUser);
            
            const today = new Date().toISOString().split('T')[0];
            const usageLimits = await UsageLimit.filter({ 
                user_email: currentUser.email, 
                date: today 
            });
            
            const todaysUsage = usageLimits.length > 0 ? usageLimits[0].count : 0;
            setUsageCount(todaysUsage);
            setIsLimitReached(todaysUsage >= DAILY_LIMIT);
        } catch (error) {
            console.log('User not logged in or usage check failed');
            setUser(null);
        }
    };

    const updateUsageCount = async () => {
        if (!user) return;
        
        try {
            const today = new Date().toISOString().split('T')[0];
            const usageLimits = await UsageLimit.filter({ 
                user_email: user.email, 
                date: today 
            });
            
            if (usageLimits.length > 0) {
                const newCount = usageLimits[0].count + 1;
                await UsageLimit.update(usageLimits[0].id, { count: newCount });
                setUsageCount(newCount);
                setIsLimitReached(newCount >= DAILY_LIMIT);
            } else {
                await UsageLimit.create({
                    user_email: user.email,
                    date: today,
                    count: 1
                });
                setUsageCount(1);
                setIsLimitReached(false);
            }
        } catch (error) {
            console.error('Error updating usage count:', error);
        }
    };

    const handleImageUpload = async (image, headline, subtext, status_tag) => {
        if (!user) {
            setError('Please log in to generate thumbnails.');
            return;
        }

        if (isLimitReached) {
            setError('Daily limit of 3 generations reached. Try again tomorrow!');
            return;
        }

        setIsProcessing(true);
        setResult(null);
        setError(null);

        try {
            console.log('Starting image upload process...');
            
            // Upload the file and get the URL
            const { file_url } = await UploadFile({ file: image.file });
            console.log('File uploaded successfully:', file_url);
            
            const thumbnailData = {
                original_image_url: file_url,
                headline: headline.trim(),
                subtext: subtext.trim(),
                status_tag: status_tag?.trim() || '',
            };

            console.log('Creating thumbnail request:', thumbnailData);
            
            // Save to database
            const createdRecord = await ThumbnailRequest.create(thumbnailData);
            console.log('Database record created:', createdRecord);
            
            // Update usage count
            await updateUsageCount();
            
            // Set the result with the database ID and generate all 3 designs
            setResult({ ...thumbnailData, id: createdRecord.id, designsToGenerate: 3 });
            
            // Smooth scroll to results
            setTimeout(() => {
                const resultsElement = document.querySelector('[data-results-section]');
                if (resultsElement) {
                    resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);

        } catch (error) {
            console.error('Error processing image:', error);
            setError('Failed to process image. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="min-h-screen bg-white">
            <HeroSection />
            
            {/* Usage Limit Warning */}
            {user && (
                <UsageLimitWarning 
                    usageCount={usageCount}
                    dailyLimit={DAILY_LIMIT}
                    isLimitReached={isLimitReached}
                />
            )}
            
            <div className="bg-white">
                <ImageUploader 
                    onImageUpload={handleImageUpload}
                    isProcessing={isProcessing}
                    user={user}
                    isLimitReached={isLimitReached}
                />
            </div>
            
            {error && (
                <div className="max-w-4xl mx-auto px-6 py-4">
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                        <p className="text-red-700 font-medium">{error}</p>
                        <button 
                            onClick={() => setError(null)}
                            className="mt-2 text-red-600 underline hover:no-underline"
                        >
                            Dismiss
                        </button>
                    </div>
                </div>
            )}
            
            <div data-results-section>
                {result && <ThumbnailResults result={result} />}
            </div>
            
            {/* Features Section */}
            <section id="features" className="py-20 bg-gray-50">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">Powerful Features</h2>
                        <p className="text-xl text-gray-600">Everything you need to create professional thumbnails</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center p-6 bg-white rounded-2xl shadow-lg">
                            <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl">🎨</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">3 Design Styles</h3>
                            <p className="text-gray-600">Luxury, Modern, and Minimal designs for every property type</p>
                        </div>
                        <div className="text-center p-6 bg-white rounded-2xl shadow-lg">
                            <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl">⚡</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">Lightning Fast</h3>
                            <p className="text-gray-600">Generate all designs in under 5 seconds with AI</p>
                        </div>
                        <div className="text-center p-6 bg-white rounded-2xl shadow-lg">
                            <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl">📱</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">High Quality</h3>
                            <p className="text-gray-600">4K resolution outputs perfect for all marketing needs</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Examples Section */}
            <section id="examples" className="py-20 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">See It In Action</h2>
                        <p className="text-xl text-gray-600">Real examples of thumbnails generated by our AI</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <div className="bg-gray-100 rounded-2xl aspect-video flex items-center justify-center">
                            <span className="text-gray-500">Luxury Style Example</span>
                        </div>
                        <div className="bg-gray-100 rounded-2xl aspect-video flex items-center justify-center">
                            <span className="text-gray-500">Modern Style Example</span>
                        </div>
                        <div className="bg-gray-100 rounded-2xl aspect-video flex items-center justify-center">
                            <span className="text-gray-500">Minimal Style Example</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing Section */}
            <section id="pricing" className="py-20 bg-gray-50">
                <div className="max-w-4xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">Simple Pricing</h2>
                        <p className="text-xl text-gray-600">Free to get started, premium features available</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-gray-200">
                            <h3 className="text-2xl font-bold text-gray-900 mb-4">Free</h3>
                            <div className="text-4xl font-bold text-gray-900 mb-2">$0</div>
                            <div className="text-gray-600 mb-6">per month</div>
                            <ul className="space-y-3 mb-8">
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    3 generations per day
                                </li>
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    All 3 design styles
                                </li>
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    4K resolution
                                </li>
                            </ul>
                            <button className="w-full py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold">
                                Get Started Free
                            </button>
                        </div>
                        <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-blue-500">
                            <h3 className="text-2xl font-bold text-gray-900 mb-4">Pro</h3>
                            <div className="text-4xl font-bold text-gray-900 mb-2">$19</div>
                            <div className="text-gray-600 mb-6">per month</div>
                            <ul className="space-y-3 mb-8">
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    Unlimited generations
                                </li>
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    All design styles
                                </li>
                                <li className="flex items-center">
                                    <span className="text-green-500 mr-2">✓</span>
                                    Priority support
                                </li>
                            </ul>
                            <button className="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
                                Upgrade to Pro
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <NextSteps />
        </div>
    );
}