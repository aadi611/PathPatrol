"""
Location utilities for geocoding and location search
"""
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from typing import List, Dict, Optional, Tuple
import time


class LocationService:
    """Service for location search and geocoding"""
    
    def __init__(self):
        """Initialize the geocoder"""
        self.geolocator = Nominatim(
            user_agent="PathPatrol_PotholeReporter/1.0",
            timeout=10
        )
        self._cache = {}
    
    def search_locations(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for locations worldwide
        
        Args:
            query: Search query (city, address, etc.)
            limit: Maximum number of results
            
        Returns:
            List of location dictionaries with display_name, lat, lon
        """
        if not query or len(query) < 2:
            return []
        
        # Check cache
        cache_key = f"{query}_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            # Search using Nominatim
            locations = self.geolocator.geocode(
                query,
                exactly_one=False,
                limit=limit,
                addressdetails=True,
                language='en'
            )
            
            if not locations:
                return []
            
            results = []
            for loc in locations:
                result = {
                    'display_name': loc.address,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'raw': loc.raw
                }
                results.append(result)
            
            # Cache the results
            self._cache[cache_key] = results
            
            # Respect API rate limits
            time.sleep(0.1)
            
            return results
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            return []
    
    def get_location_details(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Reverse geocode coordinates to get location details
        
        Args:
            latitude: Latitude
            longitude: Longitude
            
        Returns:
            Location details dictionary
        """
        try:
            location = self.geolocator.reverse(
                f"{latitude}, {longitude}",
                language='en',
                addressdetails=True
            )
            
            if location:
                return {
                    'display_name': location.address,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'raw': location.raw
                }
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address to coordinates
        
        Args:
            address: Address string
            
        Returns:
            Tuple of (latitude, longitude) or None
        """
        try:
            location = self.geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            return None
    
    def format_location_display(self, raw_location: Dict) -> str:
        """
        Format location for nice display
        
        Args:
            raw_location: Raw location data from Nominatim
            
        Returns:
            Formatted location string
        """
        address = raw_location.get('address', {})
        
        parts = []
        
        # Add road/street
        if 'road' in address:
            parts.append(address['road'])
        
        # Add suburb/neighborhood
        if 'suburb' in address:
            parts.append(address['suburb'])
        elif 'neighbourhood' in address:
            parts.append(address['neighbourhood'])
        
        # Add city
        if 'city' in address:
            parts.append(address['city'])
        elif 'town' in address:
            parts.append(address['town'])
        elif 'village' in address:
            parts.append(address['village'])
        
        # Add state/province
        if 'state' in address:
            parts.append(address['state'])
        
        # Add country
        if 'country' in address:
            parts.append(address['country'])
        
        return ', '.join(parts) if parts else raw_location.get('display_name', '')


# Global instance
location_service = LocationService()
