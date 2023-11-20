// Define the HelloWorld component
Vue.component('HelloWorld', {
    template: `
      <div>
        <h1>{{ msg }}</h1>
      </div>
    `,
    data() {
      return {
        msg: 'Hello, Vue.js!',
      };
    },
  });
  