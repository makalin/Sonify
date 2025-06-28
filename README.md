# 🎶 Sonify

Sonify is a Spotify Data Visualizer that connects to your Spotify account and generates beautiful, shareable visualizations of your listening habits. From heatmaps of your daily listening times to genre breakdowns and mood-based playlist insights — Sonify turns your data into art.

## 🚀 Features

- 🔥 **Listening heatmaps** — Discover when you listen most, visualized in stylish heatmaps.
- 🎨 **Genre & artist breakdowns** — See your top genres, artists, and tracks in vibrant charts.
- 😎 **Mood-based playlist insights** — Analyze and share the vibe of your playlists.
- 🧠 **Music Personality Analysis** — Discover what your music choices reveal about your personality.
- 📊 **Comprehensive Insights** — Deep dive into your listening patterns and music discovery habits.
- 📤 **Share-ready exports** — Download or share your data visualizations on social media.
- ⚡ **Interactive Features** — Floating action buttons, quick actions, and keyboard shortcuts.
- 📱 **Responsive Design** — Works perfectly on desktop, tablet, and mobile devices.

## 🛠 Tech Stack

- **Python** + [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) — Spotify Web API integration
- **Flask** — Lightweight web server
- **Plotly / D3.js** — Interactive and beautiful visualizations
- **Bootstrap 5** — Modern, responsive UI framework
- **Font Awesome** — Beautiful icons throughout the interface

## 🌟 Why Sonify?

While some Spotify visualizers exist, Sonify focuses on *aesthetic* insights that are perfect for sharing. Whether you're a music enthusiast or a marketer analyzing listener trends, Sonify helps you see your music data in a whole new way.

### ✨ New Features in This Version

- **🌙 Dark Theme**: Toggle between beautiful light and dark themes with smooth transitions
- **🧠 Mood Analysis**: Discover your music personality through audio features analysis
- **📊 Music Insights**: Comprehensive analysis of your listening patterns and genre preferences
- **⚡ Quick Actions**: Floating action button with instant access to key features
- **🎨 Enhanced UI**: Modern design with animations, hover effects, and interactive elements
- **📱 Mobile Optimized**: Fully responsive design that works on all devices
- **⌨️ Keyboard Shortcuts**: Quick access with keyboard shortcuts (Ctrl+K for theme, Ctrl+E for export)

## 📸 Sample Visualization

![Sample Heatmap](assets/sample_heatmap.png)

## 🏁 Getting Started

1️⃣ **Clone the repo**
```bash
git clone https://github.com/makalin/Sonify.git
cd Sonify
```

2️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

3️⃣ **Set up Spotify credentials**

Create a `.env` file:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
```

Register your app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

4️⃣ **Run the app**

```bash
flask run
```

Visit `http://localhost:5000` in your browser.

## 🎯 Key Features Explained

### 🌙 Dark Theme Support
- Toggle between light and dark themes with the moon/sun button
- Theme preference is saved in your browser
- All charts automatically adapt to the selected theme
- Smooth transitions between themes

### 🧠 Mood Analysis
- **Audio Features Radar**: Visual representation of your music characteristics
- **Personality Insights**: What your music choices reveal about you
- **Feature Breakdown**: Detailed analysis of danceability, energy, happiness, and more
- **Track Analysis**: See audio features for each of your top tracks

### 📊 Music Insights
- **Listening Patterns**: When and how often you listen to music
- **Genre Analysis**: Your top genres and music diversity
- **Artist Diversity**: How varied your music taste is
- **Playlist Analysis**: Insights about your playlist creation habits
- **Personalized Recommendations**: Tips based on your listening habits

### ⚡ Interactive Features
- **Floating Action Button**: Quick access to key features
- **Keyboard Shortcuts**: 
  - `Ctrl/Cmd + K`: Toggle theme
  - `Ctrl/Cmd + E`: Export data
  - `Escape`: Close menus
- **Hover Effects**: Interactive elements throughout the interface
- **Animations**: Smooth transitions and loading animations

## 📌 Roadmap

* [x] Add dark theme support
* [x] Add mood analysis with audio features
* [x] Add comprehensive music insights
* [x] Add interactive features and animations
* [x] Add keyboard shortcuts
* [ ] Add support for audio feature clustering
* [ ] Custom color themes for visualizations
* [ ] Multi-user dashboard
* [ ] Collaborative playlist analysis
* [ ] Music recommendation engine

## 💌 Contributing

Pull requests welcome! For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `make test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

MIT

---

**Sonify — Your music, visualized.**
