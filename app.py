import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Switch } from 'react-native';
import Slider from '@react-native-community/slider'; // Install via expo install @react-native-community/slider

export default function PersonalHandicapperApp() {
  const [region, setRegion] = useState('HK'); // 'HK' or 'ZA'
  const [activeRace, setActiveRace] = useState(1);
  const [weightForm, setWeightForm] = useState(0.5);
  const [weightPace, setWeightPace] = useState(0.5);
  const [runners, setRunners] = useState([]);
  const [mySelections, setMySelections] = useState({});

  // Simulate fetching data tailored by your slider weights
  useEffect(() => {
    // In production: fetch(`https://your-api.com{region}&race=${activeRace}&w_form=${weightForm}`)
    const mockData = [
      { id: 1, name: 'Golden Sixty', baseProb: 35, jockey: 'C.Y. Ho' },
      { id: 2, name: 'Romantic Warrior', baseProb: 28, jockey: 'J. McDonald' },
      { id: 3, name: 'California Spangle', baseProb: 20, jockey: 'B. Avdulla' },
      { id: 4, name: 'Beauty Eternal', baseProb: 17, jockey: 'Z. Purton' },
    ];
    
    // Dynamically adjust probabilities based on your custom slider inputs
    const adjusted = mockData.map(horse => {
      const modifier = (horse.id % 2 === 0) ? weightForm * 10 : weightPace * 10;
      return { ...horse, dynamicProb: Math.min(Math.max(horse.baseProb + modifier - 5, 2), 95).toFixed(1) };
    });
    
    setRunners(adjusted.sort((a, b) => b.dynamicProb - a.dynamicProb));
  }, [region, activeRace, weightForm, weightPace]);

  const toggleSelection = (id) => {
    setMySelections(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <View style={styles.container}>
      {/* Region Selector */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={[styles.regionBtn, region === 'HK' && styles.activeBtn]} 
          onPress={() => setRegion('HK')}>
          <Text style={styles.btnText}>🇭🇰 Hong Kong</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.regionBtn, region === 'ZA' && styles.activeBtn]} 
          onPress={() => setRegion('ZA')}>
          <Text style={styles.btnText}>🇿🇦 South Africa</Text>
        </TouchableOpacity>
      </View>

      {/* Horizontal Race Selector */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.raceBar}>
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
          <TouchableOpacity 
            key={num} 
            style={[styles.raceCard, activeRace === num && styles.activeRaceCard]}
            onPress={() => setActiveRace(num)}>
            <Text style={[styles.raceText, activeRace === num && styles.activeRaceText]}>R{num}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Personal AI Weighting Tuning Engine */}
      <View style={styles.sliderContainer}>
        <Text style={styles.sectionTitle}>⚙️ Tune Your Model Weights</Text>
        
        <View style={styles.sliderRow}>
          <Text style={styles.label}>Recent Form Weight: {Math.round(weightForm * 100)}%</Text>
          <Slider
            value={weightForm}
            onValueChange={setWeightForm}
            minimumValue={0}
            maximumValue={1}
            minimumTrackTintColor="#1EB1ED"
          />
        </View>

        <View style={styles.sliderRow}>
          <Text style={styles.label}>Pace / Speed Weight: {Math.round(weightPace * 100)}%</Text>
          <Slider
            value={weightPace}
            onValueChange={setWeightPace}
            minimumValue={0}
            maximumValue={1}
            minimumTrackTintColor="#1EB1ED"
          />
        </View>
      </View>

      {/* Runner Evaluation Workspace */}
      <Text style={styles.sectionTitle}>📊 AI Rankings & Your Picks</Text>
      <ScrollView style={styles.runnerList}>
        {runners.map((horse) => (
          <View key={horse.id} style={[styles.horseRow, mySelections[horse.id] && styles.selectedRow]}>
            <View style={styles.horseInfo}>
              <Text style={styles.horseName}>{horse.name}</Text>
              <Text style={styles.jockeyText}>Jockey: {horse.jockey}</Text>
            </View>
            <View style={styles.actionArea}>
              <Text style={styles.probText}>{horse.dynamicProb}%</Text>
              <Switch
                value={!!mySelections[horse.id]}
                onValueChange={() => toggleSelection(horse.id)}
                trackColor={{ false: "#767577", true: "#4cd964" }}
              />
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212', paddingTop: 50, paddingHorizontal: 15 },
  header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 15 },
  regionBtn: { flex: 0.48, padding: 12, borderRadius: 8, backgroundColor: '#1e1e1e', alignItems: 'center' },
  activeBtn: { backgroundColor: '#1EB1ED' },
  btnText: { color: '#fff', fontWeight: 'bold' },
  raceBar: { maxTransientHeight: 50, marginBottom: 15 },
  raceCard: { width: 50, height: 40, backgroundColor: '#1e1e1e', justifyContent: 'center', alignItems: 'center', marginRight: 8, borderRadius: 6 },
  activeRaceCard: { backgroundColor: '#fff' },
  raceText: { color: '#aaa', fontWeight: 'bold' },
  activeRaceText: { color: '#000' },
  sliderContainer: { backgroundColor: '#1e1e1e', padding: 15, borderRadius: 10, marginBottom: 15 },
  sectionTitle: { color: '#fff', fontSize: 16, fontWeight: 'bold', marginBottom: 10 },
  sliderRow: { marginBottom: 12 },
  label: { color: '#bbb', fontSize: 13, marginBottom: 5 },
  runnerList: { flex: 1 },
  horseRow: { flexDirection: 'row', justifyContent: 'space-between', backgroundColor: '#1e1e1e', padding: 15, borderRadius: 8, marginBottom: 8, alignItems: 'center' },
  selectedRow: { borderColor: '#4cd964', borderWidth: 1.5 },
  horseInfo: { flex: 0.65 },
  horseName: { color: '#fff', fontSize: 15, fontWeight: 'bold' },
  jockeyText: { color: '#888', fontSize: 12 },
  actionArea: { flex: 0.35, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  probText: { color: '#1EB1ED', fontWeight: 'bold', fontSize: 15 }
});
import sqlite3
import requests

DB_NAME = "my_private_racing_handicap.db"

def init_private_database():
    """Sets up a clean local database for your South African & HK historical data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS race_history (
            id TEXT PRIMARY KEY,
            region TEXT,
            track TEXT,
            race_date TEXT,
            horse_name TEXT,
            finishing_position INTEGER,
            weight_carried REAL,
            jockey_name TEXT,
            speed_rating REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("✓ Local database initialized successfully.")

def pull_historical_fixtures(region_code="HK"):
    """
    Fetches raw historical outcomes from your data feed provider 
    (e.g., The Racing API or Goalserve endpoints).
    """
    # Replace placeholder with your active programmatic data provider subscription url
    PROVIDER_URL = f"https://racingprovider.com{region_code}"
    HEADERS = {"Authorization": "Bearer YOUR_API_SECRET_KEY"}
    
    try:
        response = requests.get(PROVIDER_URL, headers=HEADERS)
        if response.status_code == 200:
            raw_races = response.json().get("data", [])
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            for entry in raw_races:
                cursor.execute('''
                    INSERT OR IGNORE INTO race_history 
                    (id, region, track, race_date, horse_name, finishing_position, weight_carried, jockey_name, speed_rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    f"{region_code}_{entry['race_id']}_{entry['horse_id']}",
                    region_code,
                    entry['venue'],
                    entry['date'],
                    entry['horse'],
                    entry['position'],
                    entry['weight'],
                    entry['jockey'],
                    entry['speed_figure']
                ))
            
            conn.commit()
            conn.close()
            print(f"✓ Successfully synced {len(raw_races)} past runs into your private dataset.")
    except Exception as e:
        print(f"Error handling live pipeline extraction: {e}")

# Run setup
init_private_database()
# pull_historical_fixtures("HK")
