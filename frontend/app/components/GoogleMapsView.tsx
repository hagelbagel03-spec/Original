import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

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

  const openInGoogleMaps = () => {
    const url = `https://www.google.com/maps?q=${coordinates.lat},${coordinates.lng}`;
    if (Platform.OS === 'web') {
      // @ts-ignore
      window.open(url, '_blank');
    }
  };

  return (
    <View style={styles.container}>
      {/* Interactive Google Maps für Web */}
      {Platform.OS === 'web' ? (
        <iframe
          src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyDummy_Key_For_Development&q=${coordinates.lat},${coordinates.lng}&zoom=16`}
          width="100%"
          height="100%"
          style={{ border: 0, borderRadius: 12 }}
          allowFullScreen
          loading="lazy"
        />
      ) : (
        <View style={styles.nativeMapPlaceholder}>
          <Ionicons name="map" size={48} color={colors.primary} />
          <Text style={styles.mapTitle}>🗺️ Live Google Maps</Text>
          <Text style={styles.mapSubtitle}>📍 {incident.address}</Text>
          <Text style={styles.coordinates}>
            📍 {coordinates.lat.toFixed(6)}, {coordinates.lng.toFixed(6)}
          </Text>
          
          <TouchableOpacity 
            style={styles.openMapsButton}
            onPress={openInGoogleMaps}
          >
            <Ionicons name="navigate" size={20} color="#FFFFFF" />
            <Text style={styles.openMapsText}>In Google Maps öffnen</Text>
          </TouchableOpacity>
        </View>
      )}
      
      {/* Info Overlay nur für Web */}
      {Platform.OS === 'web' && (
        <View style={styles.infoOverlay}>
          <View style={[styles.priorityBadge, {
            backgroundColor: getPriorityColor(incident.priority)
          }]}>
            <Text style={styles.priorityText}>
              {incident.priority?.toUpperCase() || 'NORMAL'} PRIORITÄT
            </Text>
          </View>
          <Text style={styles.addressText}>📍 {incident.address}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 8,
    height: 300,
  },
  map: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  infoOverlay: {
    position: 'absolute',
    top: 10,
    left: 10,
    right: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    padding: 12,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  priorityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  priorityText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  addressText: {
    fontSize: 14,
    color: '#1a1a1a',
    fontWeight: '500',
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