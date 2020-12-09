import colors from "vuetify/es5/util/colors";

let dynamicRoutes = () => {
  return new Promise.all([
    fetch(process.env.NUXT_ENV_WORKSHOPS + "/getWorkshops"),
  ])
    .then((resp) => resp.json())
    .then((data) => {
      return data.map((line) => `/app/workshop/${line.index}`);
    });
};

export default {
    // Target (https://go.nuxtjs.dev/config-target)
    target: "static",

    // Global page headers (https://go.nuxtjs.dev/config-head)
    head: {
        title: "Vueducation",
        meta: [
            { charset: "utf-8" },
            { name: "viewport", content: "width=device-width, initial-scale=1" },
            { hid: "description", name: "description", content: "" },
        ],
        link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },

    // Global CSS (https://go.nuxtjs.dev/config-css)
    css: ["@fortawesome/fontawesome-free/css/all.css"],
    // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
    plugins: [
        { src: "~/plugins/vue-youtube-embed.js", mode: "client" },
        { src: "~/plugins/vue-stripe-checkout.js", ssr: false },
        { src: "@/plugins/aos", mode: "client" },
        { src: "~/plugins/vue-notification.js", ssr: false },
    ],

    // Auto import components (https://go.nuxtjs.dev/config-components)
    components: true,

    // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
    buildModules: [
        // https://go.nuxtjs.dev/vuetify
        "@nuxtjs/vuetify",
    ],

    // Modules (https://go.nuxtjs.dev/config-modules)
    modules: [
        // https://go.nuxtjs.dev/axios
        "@nuxtjs/axios",
        // https://go.nuxtjs.dev/pwa
        "@nuxtjs/pwa",
        // https://go.nuxtjs.dev/content
        "@nuxt/content",
        // https://auth.nuxtjs.org/
        "@nuxtjs/auth",
        [
            "@nuxtjs/firebase",
            {
                config: {
                    apiKey: "AIzaSyAMLAGrtX-WBSFIMYwgzoTp1ghEQK-Bp4Y",
                    authDomain: "vueducation-48372.firebaseapp.com",
                    databaseURL: "https://vueducation-48372.firebaseio.com",
                    projectId: "vueducation-48372",
                    storageBucket: "vueducation-48372.appspot.com",
                    messagingSenderId: "<messagingSenderId>",
                    appId: "100313885646",
                },
                services: {
                    firestore: true,
                },
            },
        ],
    ],

    // Axios module configuration (https://go.nuxtjs.dev/config-axios)
    axios: {
        proxy: true,
        credentials: false,
    },

    proxy: {
        // Note: In the proxy module, /api/ will be added to all requests to the API end point. If you need to remove it use the pathRewrite option:
        "/api/": {
            target: process.env.NUXT_ENV_BACKEND,
            pathRewrite: { "^/api/": "" },
        },
    },

    vuetify: {
        defaultAssets: { icons: "fa" },
    },

    // Content module configuration (https://go.nuxtjs.dev/content-config)
    content: {},

    // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
    vuetify: {
        customVariables: ["~/assets/variables.scss"],
        theme: {
            dark: false,
            themes: {
                dark: {
                    primary: colors.blue.darken2,
                    accent: colors.grey.darken3,
                    secondary: colors.amber.darken3,
                    info: colors.teal.lighten1,
                    warning: colors.amber.base,
                    error: colors.deepOrange.accent4,
                    success: colors.green.accent3,
                },
            },
        },
    },

    // Build Configuration (https://go.nuxtjs.dev/config-build)
    build: {
        devMiddleware: {
            headers: {
                "Cache-Control": "no-store",
                Vary: "*",
            },
        },
    },

    // Env variables
    env: {
        STRIPE_PK: process.env.STRIPE_PK,
    },

    auth: {
        redirect: {
            login: "/app/login",
            logout: "/app/login",
            home: "/app",
        },
        strategies: {
            local: {
                endpoints: {
                    login: { url: "/api/auth/login", method: "post", propertyName: "token" },
                    logout: false,
                    user: { url: "/api/auth/me", method: "get", propertyName: "user" },
                },
                tokenType: "",
            },
        },
    },
    // generate dynamic routes
    generate: {
        routes: dynamicRoutes,
    },
};
