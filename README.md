# 🌱 PlantVision - Discover the Nature Around You

PlantVision is a beautiful, responsive web application that helps users identify and learn about plants using the Perenual Plant API. Simply search for any plant name and discover detailed information including care requirements, scientific names, and beautiful imagery.

## ✨ Features

- 🔍 **Plant Search**: Search for plants by common name, scientific name, or other names
- 📱 **Responsive Design**: Beautiful UI that works seamlessly on desktop and mobile
- 🖼️ **Image Gallery**: High-quality plant images with zoom functionality
- 💧 **Care Information**: Watering needs and sunlight requirements
- 📋 **Detailed Info**: Scientific names, alternative names, and care badges
- 🎨 **Modern UI**: Soft green tones, smooth animations, and elegant cards
- ⚡ **Fast Loading**: Optimized performance with loading states and error handling

## 🚀 Live Demo

Experience PlantVision in action - search for plants like "Rose", "Monstera", or "Lavender"!

## 🛠️ Technologies Used

This project is built with modern web technologies:

- **React 18** - Component-based UI library
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible component library
- **Lucide React** - Clean, customizable icons
- **Perenual API** - Comprehensive plant database

## 🎯 Getting Started

### Prerequisites

- Node.js 16+ and npm installed
- Get a free API key from [Perenual](https://perenual.com/docs/api)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PlantVision.git
   cd PlantVision
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Add your API key**
   - Update the API key in `src/services/plantApi.ts`
   - Replace `YOUR_API_KEY` with your Perenual API key

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   - Navigate to `http://localhost:5173`
   - Start searching for plants!

## 📁 Project Structure

```
PlantVision/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── PlantCard.tsx    # Individual plant display
│   │   ├── PlantResults.tsx # Search results grid
│   │   └── PlantSearch.tsx  # Search input component
│   ├── services/
│   │   └── plantApi.ts      # Perenual API integration
│   ├── pages/
│   │   └── Index.tsx        # Main application page
│   └── index.css            # Global styles and design tokens
├── public/                  # Static assets
└── README.md
```

## 🌿 Usage

1. **Search Plants**: Enter any plant name in the search box
2. **View Results**: Browse up to 3 matching plants in beautiful cards
3. **Explore Details**: Click "More details" to see additional information
4. **Zoom Images**: Click on plant images to view them in full size
5. **Learn Care**: Check watering and sunlight requirement badges

## 🎨 Design System

PlantVision uses a carefully crafted design system with:

- **Color Palette**: Soft greens, earth tones, and clean whites
- **Typography**: Modern, readable fonts with proper hierarchy
- **Spacing**: Consistent rhythm and breathing room
- **Animations**: Smooth transitions and fade-in effects
- **Responsive**: Mobile-first approach with tablet and desktop optimizations

## 🔧 Customization

### Adding New Features

The codebase is modular and easy to extend:

- Add new plant data fields in `PlantData` interface
- Create custom UI components in `components/ui/`
- Extend the API service for additional endpoints
- Customize the design system in `index.css` and `tailwind.config.ts`

### API Configuration

Update `src/services/plantApi.ts` to:
- Change API endpoints
- Modify search parameters
- Add error handling
- Implement caching

## 📱 Deployment

### Build for Production

```bash
npm run build
```

The optimized build will be created in the `dist/` directory.

### Deploy Options

- **Vercel**: Connect your GitHub repo for automatic deployments
- **Netlify**: Drag and drop the `dist` folder
- **GitHub Pages**: Use GitHub Actions for CI/CD
- **Any static hosting**: Upload the `dist` folder contents

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Perenual API** - For providing comprehensive plant data
- **shadcn/ui** - For beautiful, accessible components
- **Unsplash** - For fallback plant imagery
- **Lucide** - For clean, consistent icons

## 📧 Contact

Have questions or suggestions? Feel free to reach out!

---

**Built with ❤️ for plant enthusiasts everywhere** 🌿