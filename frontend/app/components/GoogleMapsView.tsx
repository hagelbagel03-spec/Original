import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';

const GoogleMapsView = ({ incident }: { incident: any }) => {
  const colors = {
    text: '#1a1a1a',
    textMuted: '#6c757d',
    background: '#ffffff',
    surface: '#f8f9fa',
    border: '#e9ecef',
    primary: '#2196F3',
    error: '#DC3545',
    warning: '#FFC107',
    success: '#28A745'
  };

  const getCoordinates = () => {
    if (incident?.location?.lat && incident?.location?.lng) {
      return {
        lat: parseFloat(incident.location.lat),
        lng: parseFloat(incident.location.lng)
      };
    }
    if (incident?.coordinates?.lat && incident?.coordinates?.lng) {
      return {
        lat: parseFloat(incident.coordinates.lat),
        lng: parseFloat(incident.coordinates.lng)
      };
    }
    return null;
  };

  const coordinates = getCoordinates();

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high': return colors.error;
      case 'medium': return colors.warning;
      case 'low': return colors.success;
      default: return colors.primary;
    }
  };

  if (!coordinates) {
    return (
      <View style={styles.container}>
        <View style={styles.noLocationContainer}>
          <Ionicons name="location-outline" size={32} color={colors.textMuted} />
          <Text style={styles.noLocationText}>
            Keine GPS-Koordinaten verfügbar
          </Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.mapContainer}>
        <View style={styles.mapView}>
          <Ionicons name="map" size={32} color={colors.primary} />
          <Text style={styles.mapTitle}>🗺️ Live-Karte</Text>
          <Text style={styles.mapSubtitle}>
            📍 {incident.address}
          </Text>
          <Text style={styles.mapCoordinates}>
            {coordinates.lat.toFixed(6)}, {coordinates.lng.toFixed(6)}
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 8,
  },
  mapContainer: {
    minHeight: 200,
  },
  mapView: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#2196F3',
    margin: 16,
    borderRadius: 12,
    minHeight: 150,
  },
  mapTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 8,
    textAlign: 'center',
  },
  mapSubtitle: {
    fontSize: 14,
    color: '#ffffff',
    marginTop: 4,
    textAlign: 'center',
    opacity: 0.9,
  },
  mapCoordinates: {
    fontSize: 12,
    color: '#ffffff',
    marginTop: 8,
    fontFamily: 'monospace',
    textAlign: 'center',
    opacity: 0.8,
  },
  incidentTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginTop: 12,
    textAlign: 'center',
  },
  incidentAddress: {
    fontSize: 14,
    color: '#6c757d',
    marginTop: 4,
    textAlign: 'center',
  },
  coordinates: {
    fontSize: 12,
    color: '#6c757d',
    marginTop: 8,
    fontFamily: 'monospace',
    textAlign: 'center',
  },
  priorityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginTop: 12,
  },
  priorityText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  noLocationContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
    backgroundColor: '#f8f9fa',
  },
  noLocationText: {
    fontSize: 14,
    color: '#6c757d',
    marginTop: 8,
    textAlign: 'center',
  },
});

export default GoogleMapsView;