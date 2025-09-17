// Chat state reset script - run this in browser console
console.log('Clearing all chat data...');

// Clear localStorage
localStorage.clear();

// Clear sessionStorage  
sessionStorage.clear();

// Reload the page
window.location.reload(true);

console.log('Chat state cleared! Page will reload...');
