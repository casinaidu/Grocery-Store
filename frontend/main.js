// Import the HelloWorld component
import HelloWorld from './components/HelloWorld.js';

// Create a new Vue instance
new Vue({
  el: '#app',
  template: `
    <div>
      <HelloWorld />
    </div>
  `,
  // Register the HelloWorld component
  components: {
    HelloWorld,
  },
});
