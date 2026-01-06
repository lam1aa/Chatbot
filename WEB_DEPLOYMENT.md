# Web Deployment Guide

## GitHub Pages Deployment

This chatbot can be deployed as a static web application on GitHub Pages, allowing you to share it with others via a simple link.

### 🌐 Live Demo

Once deployed, your chatbot will be available at:
```
https://<username>.github.io/Chatbot/
```

### 📋 Deployment Steps

#### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `main` (or your default branch)
   - Folder: `/ (root)`
4. Click **Save**

#### 2. Wait for Deployment

GitHub will automatically build and deploy your site. This usually takes 1-2 minutes.

You can check the deployment status:
- Go to **Actions** tab in your repository
- Look for "pages build and deployment" workflow

#### 3. Access Your Chatbot

Once deployed, visit:
```
https://<username>.github.io/Chatbot/
```

Replace `<username>` with your GitHub username.

### 🔑 User Setup

Users who visit your chatbot will need to:

1. Create a free account at [OpenRouter.ai](https://openrouter.ai/)
2. Get their API key from the OpenRouter dashboard
3. Enter the API key in the web interface

**Note:** Each user needs their own API key. The key is stored locally in their browser and never sent to your server.

### 🛠️ Customization

#### Change the Chatbot Prompt

Edit `app.js` and modify the `systemPrompt` variable:

```javascript
const systemPrompt = `Your custom instructions here...`;
```

#### Change the Model

In `app.js`, find this line:

```javascript
model: 'meta-llama/llama-3.1-8b-instruct:free',
```

You can change it to any model available on OpenRouter. See [OpenRouter Models](https://openrouter.ai/models) for options.

#### Customize Styling

Edit `styles.css` to change colors, fonts, and layout.

### 📱 Mobile Support

The web interface is fully responsive and works on mobile devices, tablets, and desktops.

### 🔒 Security Notes

- API keys are stored only in the user's browser (localStorage)
- All communication is done directly between the user's browser and OpenRouter
- No server-side code is required
- No user data is collected or stored on GitHub Pages

### 🐛 Troubleshooting

#### Pages not deploying?

1. Check that you have `index.html`, `styles.css`, and `app.js` in the root directory
2. Verify GitHub Pages is enabled in repository settings
3. Check the Actions tab for build errors

#### Chatbot not working?

1. Open browser developer console (F12) to check for errors
2. Verify the API key is valid
3. Check that you have internet connectivity
4. Ensure the OpenRouter API is accessible

### 📚 Related Files

- `index.html` - Main HTML structure
- `styles.css` - Styling and responsive design
- `app.js` - JavaScript application logic
