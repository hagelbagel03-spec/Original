import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
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

  return (
    <View style={styles.container}>
      <View style={styles.mapContainer}>
        <View style={styles.mapPlaceholder}>
          <Ionicons name="location" size={48} color={getPriorityColor(incident.priority)} />
          <Text style={styles.incidentTitle}>📍 {incident.title}</Text>
          <Text style={styles.incidentAddress}>{incident.address}</Text>
          <Text style={styles.coordinates}>
            🧭 {coordinates.lat.toFixed(6)}, {coordinates.lng.toFixed(6)}
          </Text>
          
          <View style={[styles.priorityBadge, {
            backgroundColor: getPriorityColor(incident.priority)
          }]}>
            <Text style={styles.priorityText}>
              {incident.priority?.toUpperCase() || 'NORMAL'} PRIORITÄT
            </Text>
          </View>
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
  mapPlaceholder: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    backgroundColor: '#f8f9fa',
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: '#e9ecef',
    margin: 16,
    borderRadius: 12,
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