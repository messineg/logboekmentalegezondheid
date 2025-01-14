// ecosystem.config.js
module.exports = {
    apps: [{
      name: 'django-app',
      script: 'start_django.bat',
      watch: false,  // Disable watch to prevent restarts
      windowsHide: true
    }]
  };