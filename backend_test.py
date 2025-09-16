#!/usr/bin/env python3
"""
Backend Test Suite for SOS System with GPS Functionality
Tests the emergency broadcast system and GPS data handling
"""

import requests
import json
import time
from datetime import datetime
import sys

# Test configuration
BASE_URL = "http://localhost:8001/api"
TEST_USER = {
    "email": "test@stadtwache.de",
    "password": "admin123"
}

# Test GPS data
TEST_GPS_DATA = {
    "latitude": 51.4818,
    "longitude": 7.2162,
    "accuracy": 5
}

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_data = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def setup_authentication(self):
        """Setup authentication for tests"""
        print("\n🔐 Setting up authentication...")
        
        try:
            # First, try to create the test user (in case it doesn't exist)
            register_data = {
                "email": TEST_USER["email"],
                "username": "Test User",
                "password": TEST_USER["password"],
                "role": "admin"
            }
            
            register_response = self.session.post(
                f"{BASE_URL}/auth/register",
                json=register_data,
                timeout=10
            )
            
            if register_response.status_code == 200:
                print("✅ Test user created successfully")
            elif register_response.status_code == 400 and "already registered" in register_response.text:
                print("ℹ️  Test user already exists")
            else:
                print(f"⚠️  User creation response: {register_response.status_code}")
            
        except Exception as e:
            print(f"⚠️  User creation failed: {e}")
        
        # Now login
        try:
            login_response = self.session.post(
                f"{BASE_URL}/auth/login",
                json=TEST_USER,
                timeout=10
            )
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                self.auth_token = login_data["access_token"]
                self.user_data = login_data["user"]
                
                # Set authorization header for future requests
                self.session.headers.update({
                    "Authorization": f"Bearer {self.auth_token}"
                })
                
                self.log_test(
                    "Authentication Setup",
                    True,
                    f"Successfully authenticated as {self.user_data['username']}"
                )
                return True
            else:
                self.log_test(
                    "Authentication Setup",
                    False,
                    f"Login failed with status {login_response.status_code}",
                    login_response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Authentication Setup",
                False,
                f"Authentication error: {str(e)}"
            )
            return False
    
    def test_emergency_broadcast_with_gps(self):
        """Test emergency broadcast with GPS data"""
        print("\n🚨 Testing Emergency Broadcast with GPS...")
        
        try:
            alert_data = {
                "type": "sos_alarm",
                "message": "Test SOS Alarm mit GPS-Daten",
                "priority": "urgent",
                "location": TEST_GPS_DATA,
                "location_status": "GPS verfügbar"
            }
            
            response = self.session.post(
                f"{BASE_URL}/emergency/broadcast",
                json=alert_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify response structure
                required_fields = ["success", "broadcast_id", "location_transmitted", "location_status"]
                missing_fields = [field for field in required_fields if field not in result]
                
                if missing_fields:
                    self.log_test(
                        "Emergency Broadcast with GPS",
                        False,
                        f"Missing fields in response: {missing_fields}",
                        result
                    )
                    return False
                
                # Verify GPS data was transmitted
                if result.get("location_transmitted") != True:
                    self.log_test(
                        "Emergency Broadcast with GPS",
                        False,
                        "GPS data was not transmitted correctly",
                        result
                    )
                    return False
                
                self.log_test(
                    "Emergency Broadcast with GPS",
                    True,
                    f"Emergency broadcast created successfully (ID: {result['broadcast_id']})"
                )
                return result["broadcast_id"]
            else:
                self.log_test(
                    "Emergency Broadcast with GPS",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Emergency Broadcast with GPS",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_emergency_broadcast_without_gps(self):
        """Test emergency broadcast without GPS data (fallback)"""
        print("\n🚨 Testing Emergency Broadcast without GPS (Fallback)...")
        
        try:
            alert_data = {
                "type": "sos_alarm",
                "message": "Test SOS Alarm ohne GPS-Daten",
                "priority": "urgent",
                "location": None,
                "location_status": "GPS nicht verfügbar"
            }
            
            response = self.session.post(
                f"{BASE_URL}/emergency/broadcast",
                json=alert_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify response structure
                if not result.get("success"):
                    self.log_test(
                        "Emergency Broadcast without GPS",
                        False,
                        "Broadcast was not successful",
                        result
                    )
                    return False
                
                # Verify GPS data was not transmitted (fallback scenario)
                if result.get("location_transmitted") != False:
                    self.log_test(
                        "Emergency Broadcast without GPS",
                        False,
                        "Expected location_transmitted to be False for fallback scenario",
                        result
                    )
                    return False
                
                self.log_test(
                    "Emergency Broadcast without GPS",
                    True,
                    f"Fallback emergency broadcast created successfully (ID: {result['broadcast_id']})"
                )
                return result["broadcast_id"]
            else:
                self.log_test(
                    "Emergency Broadcast without GPS",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Emergency Broadcast without GPS",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_get_emergency_broadcasts(self):
        """Test retrieving emergency broadcasts"""
        print("\n📡 Testing Emergency Broadcasts Retrieval...")
        
        try:
            response = self.session.get(
                f"{BASE_URL}/emergency/broadcasts",
                timeout=10
            )
            
            if response.status_code == 200:
                broadcasts = response.json()
                
                if not isinstance(broadcasts, list):
                    self.log_test(
                        "Get Emergency Broadcasts",
                        False,
                        "Response is not a list",
                        broadcasts
                    )
                    return False
                
                # Check if we have broadcasts (should have at least the ones we created)
                if len(broadcasts) == 0:
                    self.log_test(
                        "Get Emergency Broadcasts",
                        False,
                        "No emergency broadcasts found",
                        "Expected to find previously created broadcasts"
                    )
                    return False
                
                # Verify broadcast structure
                for broadcast in broadcasts:
                    required_fields = ["id", "type", "message", "sender_id", "sender_name", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in broadcast]
                    
                    if missing_fields:
                        self.log_test(
                            "Get Emergency Broadcasts",
                            False,
                            f"Broadcast missing required fields: {missing_fields}",
                            broadcast
                        )
                        return False
                
                self.log_test(
                    "Get Emergency Broadcasts",
                    True,
                    f"Successfully retrieved {len(broadcasts)} emergency broadcasts"
                )
                return broadcasts
            else:
                self.log_test(
                    "Get Emergency Broadcasts",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Get Emergency Broadcasts",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_gps_data_persistence(self, broadcast_id):
        """Test that GPS data is correctly stored in MongoDB"""
        print("\n💾 Testing GPS Data Persistence...")
        
        try:
            # Get the broadcasts and find our specific one
            broadcasts = self.test_get_emergency_broadcasts()
            if not broadcasts:
                self.log_test(
                    "GPS Data Persistence",
                    False,
                    "Could not retrieve broadcasts to verify GPS data persistence"
                )
                return False
            
            # Find the broadcast with GPS data
            gps_broadcast = None
            for broadcast in broadcasts:
                if broadcast.get("id") == broadcast_id and broadcast.get("has_gps"):
                    gps_broadcast = broadcast
                    break
            
            if not gps_broadcast:
                self.log_test(
                    "GPS Data Persistence",
                    False,
                    f"Could not find broadcast with ID {broadcast_id} and GPS data"
                )
                return False
            
            # Verify GPS data structure
            location = gps_broadcast.get("location")
            if not location:
                self.log_test(
                    "GPS Data Persistence",
                    False,
                    "GPS location data not found in stored broadcast"
                )
                return False
            
            # Verify GPS coordinates match what we sent
            expected_lat = TEST_GPS_DATA["latitude"]
            expected_lng = TEST_GPS_DATA["longitude"]
            expected_accuracy = TEST_GPS_DATA["accuracy"]
            
            if (location.get("latitude") != expected_lat or 
                location.get("longitude") != expected_lng or
                location.get("accuracy") != expected_accuracy):
                self.log_test(
                    "GPS Data Persistence",
                    False,
                    "GPS coordinates don't match expected values",
                    f"Expected: {TEST_GPS_DATA}, Got: {location}"
                )
                return False
            
            self.log_test(
                "GPS Data Persistence",
                True,
                "GPS data correctly stored and retrieved from database"
            )
            return True
            
        except Exception as e:
            self.log_test(
                "GPS Data Persistence",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_app_crash_resilience(self):
        """Test that app doesn't crash with GPS problems"""
        print("\n🛡️  Testing App Crash Resilience with GPS Problems...")
        
        try:
            # Test with malformed GPS data
            malformed_tests = [
                {
                    "name": "Invalid GPS coordinates",
                    "data": {
                        "type": "sos_alarm",
                        "message": "Test mit ungültigen GPS-Daten",
                        "location": {"latitude": "invalid", "longitude": "invalid"},
                        "location_status": "GPS Fehler"
                    }
                },
                {
                    "name": "Missing GPS fields",
                    "data": {
                        "type": "sos_alarm", 
                        "message": "Test mit fehlenden GPS-Feldern",
                        "location": {"latitude": 51.4818},  # Missing longitude
                        "location_status": "GPS unvollständig"
                    }
                },
                {
                    "name": "Empty GPS object",
                    "data": {
                        "type": "sos_alarm",
                        "message": "Test mit leerem GPS-Objekt",
                        "location": {},
                        "location_status": "GPS leer"
                    }
                }
            ]
            
            all_passed = True
            for test in malformed_tests:
                try:
                    response = self.session.post(
                        f"{BASE_URL}/emergency/broadcast",
                        json=test["data"],
                        timeout=10
                    )
                    
                    # App should handle gracefully (either accept or reject, but not crash)
                    if response.status_code in [200, 400, 422]:  # Acceptable responses
                        print(f"  ✅ {test['name']}: Handled gracefully (status {response.status_code})")
                    else:
                        print(f"  ❌ {test['name']}: Unexpected status {response.status_code}")
                        all_passed = False
                        
                except requests.exceptions.ConnectionError:
                    print(f"  ❌ {test['name']}: App crashed or became unresponsive")
                    all_passed = False
                except Exception as e:
                    print(f"  ❌ {test['name']}: Exception: {str(e)}")
                    all_passed = False
            
            self.log_test(
                "App Crash Resilience",
                all_passed,
                "App handles GPS problems gracefully" if all_passed else "App has issues with malformed GPS data"
            )
            return all_passed
            
        except Exception as e:
            self.log_test(
                "App Crash Resilience",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SOS System Backend Tests...")
        print("=" * 60)
        
        # Setup authentication
        if not self.setup_authentication():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return False
        
        # Test emergency broadcast with GPS
        gps_broadcast_id = self.test_emergency_broadcast_with_gps()
        
        # Test emergency broadcast without GPS (fallback)
        fallback_broadcast_id = self.test_emergency_broadcast_without_gps()
        
        # Test retrieving emergency broadcasts
        self.test_get_emergency_broadcasts()
        
        # Test GPS data persistence
        if gps_broadcast_id:
            self.test_gps_data_persistence(gps_broadcast_id)
        
        # Test app crash resilience
        self.test_app_crash_resilience()
        
        # Print summary
        self.print_summary()
        
        return self.get_overall_success()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
    
    def get_overall_success(self):
        """Get overall test success status"""
        return all(result["success"] for result in self.test_results)

def main():
    """Main test execution"""
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()