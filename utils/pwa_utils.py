"""
PWA (Progressive Web App) utilities for PathPatrol
Handles service worker registration, push notifications, and offline functionality
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path


def inject_pwa_code():
    """
    Inject PWA-related code into the Streamlit app
    Includes manifest, service worker registration, and install prompt
    """
    
    # Get the base path
    base_path = Path(__file__).parent.parent / 'static'
    
    pwa_html = """
    <script>
        // Register Service Worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/service-worker.js')
                    .then((registration) => {
                        console.log('ServiceWorker registered:', registration.scope);
                        
                        // Check for updates
                        registration.addEventListener('updatefound', () => {
                            const newWorker = registration.installing;
                            newWorker.addEventListener('statechange', () => {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    // New version available
                                    if (confirm('New version available! Reload to update?')) {
                                        newWorker.postMessage({ type: 'SKIP_WAITING' });
                                        window.location.reload();
                                    }
                                }
                            });
                        });
                    })
                    .catch((error) => {
                        console.log('ServiceWorker registration failed:', error);
                    });
            });
        }
        
        // Install prompt
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show custom install button
            const installButton = document.getElementById('pwa-install-button');
            if (installButton) {
                installButton.style.display = 'block';
            }
        });
        
        // Handle install button click
        function installPWA() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                });
            }
        }
        
        // Request notification permission
        function requestNotificationPermission() {
            if ('Notification' in window) {
                Notification.requestPermission().then((permission) => {
                    if (permission === 'granted') {
                        console.log('Notification permission granted');
                        
                        // Subscribe to push notifications
                        navigator.serviceWorker.ready.then((registration) => {
                            const applicationServerKey = urlBase64ToUint8Array(
                                'YOUR_PUBLIC_VAPID_KEY_HERE'  // Replace with actual VAPID key
                            );
                            
                            registration.pushManager.subscribe({
                                userVisibleOnly: true,
                                applicationServerKey: applicationServerKey
                            }).then((subscription) => {
                                console.log('Push subscription:', subscription);
                                // Send subscription to server
                                // sendSubscriptionToServer(subscription);
                            }).catch((error) => {
                                console.log('Failed to subscribe to push:', error);
                            });
                        });
                    }
                });
            }
        }
        
        // Helper function to convert VAPID key
        function urlBase64ToUint8Array(base64String) {
            const padding = '='.repeat((4 - base64String.length % 4) % 4);
            const base64 = (base64String + padding)
                .replace(/\-/g, '+')
                .replace(/_/g, '/');
            
            const rawData = window.atob(base64);
            const outputArray = new Uint8Array(rawData.length);
            
            for (let i = 0; i < rawData.length; ++i) {
                outputArray[i] = rawData.charCodeAt(i);
            }
            return outputArray;
        }
        
        // Check if app is installed
        window.addEventListener('appinstalled', () => {
            console.log('PathPatrol PWA was installed');
            // Hide install button
            const installButton = document.getElementById('pwa-install-button');
            if (installButton) {
                installButton.style.display = 'none';
            }
        });
        
        // Detect if running as PWA
        function isPWA() {
            return window.matchMedia('(display-mode: standalone)').matches ||
                   window.navigator.standalone === true;
        }
        
        // Show PWA status
        if (isPWA()) {
            console.log('Running as PWA');
        } else {
            console.log('Running in browser');
        }
        
        // Offline/Online detection
        window.addEventListener('online', () => {
            console.log('Back online');
            // Show notification or sync data
        });
        
        window.addEventListener('offline', () => {
            console.log('Gone offline');
            // Show offline indicator
        });
    </script>
    
    <style>
        /* PWA Install Button */
        #pwa-install-button {
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            padding: 15px 30px;
            background: linear-gradient(135deg, #16c79a 0%, #0f9876 100%);
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(22, 199, 154, 0.4);
            transition: all 0.3s ease;
            animation: pulse-install 2s infinite;
        }
        
        #pwa-install-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(22, 199, 154, 0.6);
        }
        
        @keyframes pulse-install {
            0%, 100% {
                box-shadow: 0 4px 15px rgba(22, 199, 154, 0.4);
            }
            50% {
                box-shadow: 0 4px 25px rgba(22, 199, 154, 0.8);
            }
        }
        
        /* Offline indicator */
        .offline-indicator {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff4c4c;
            color: white;
            text-align: center;
            padding: 10px;
            font-weight: 600;
            z-index: 10000;
            display: none;
        }
        
        .offline-indicator.show {
            display: block;
        }
    </style>
    
    <button id="pwa-install-button" onclick="installPWA()">
        📱 Install PathPatrol App
    </button>
    
    <div class="offline-indicator" id="offline-indicator">
        🚧 You're offline - Some features may be limited
    </div>
    
    <script>
        // Show/hide offline indicator
        function updateOfflineIndicator() {
            const indicator = document.getElementById('offline-indicator');
            if (indicator) {
                if (navigator.onLine) {
                    indicator.classList.remove('show');
                } else {
                    indicator.classList.add('show');
                }
            }
        }
        
        window.addEventListener('online', updateOfflineIndicator);
        window.addEventListener('offline', updateOfflineIndicator);
        updateOfflineIndicator();
    </script>
    """
    
    components.html(pwa_html, height=0)


def add_manifest_link():
    """Add manifest link to the page"""
    manifest_html = """
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#0f3460">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="PathPatrol">
    <link rel="apple-touch-icon" href="/static/icons/icon-192x192.png">
    """
    components.html(manifest_html, height=0)


def render_pwa_install_prompt():
    """Render a custom install prompt in the UI"""
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #16c79a 0%, #0f9876 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    '>
        <h3 style='color: white; margin: 0 0 10px 0;'>📱 Install PathPatrol</h3>
        <p style='color: white; margin: 0 0 15px 0;'>
            Add PathPatrol to your home screen for quick access and offline use!
        </p>
        <button onclick='installPWA()' style='
            background: white;
            color: #0f9876;
            border: none;
            padding: 10px 30px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            font-size: 16px;
        '>
            Install Now
        </button>
    </div>
    """, unsafe_allow_html=True)


def check_pwa_status():
    """Check if app is running as PWA"""
    pwa_check = """
    <script>
        if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
            window.parent.postMessage({type: 'pwa-status', isPWA: true}, '*');
        } else {
            window.parent.postMessage({type: 'pwa-status', isPWA: false}, '*');
        }
    </script>
    """
    components.html(pwa_check, height=0)


def enable_push_notifications():
    """Enable push notification subscription"""
    
    if 'notification_enabled' not in st.session_state:
        st.session_state.notification_enabled = False
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("**Enable notifications to get updates on your complaints**")
    
    with col2:
        if st.button("🔔 Enable", key="enable_notifications"):
            # This will trigger the browser notification permission
            notification_js = """
            <script>
                requestNotificationPermission();
            </script>
            """
            components.html(notification_js, height=0)
            st.session_state.notification_enabled = True
            st.success("Notification permission requested!")
