/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {

    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        colors: {
            black: "#15171A",
            white: "#FFFFFF",
            primary: {
                blue: {
                    800: "#0B3C93",
                    700: "#105ADC",
                    600: "#3F80F1",
                    500: "#7FAAF6",
                    400: "#BAD1F8",
                    300: "#BFD5FA",
                    200: "#DFEAFD",
                    100: "#F2F7FF",
                },
            },
            secondary: {
                blue: {
                    darkest: "#141457",
                    dark: "#2C2C68",
                    light: "#494986",
                    lightest: "#A6A7CC",
                },
                orange: {
                    dark: "#E89423",
                    regular: "#ffa42b",
                    light: "#ffd399",
                }
            },
            notifications: {
                success: {
                    regular: "#3bb385",
                    light: "#d8f5e9",
                },
                warning: {
                    regular: "#ffd32a",
                    light: "#fff4cc",
                },
                error: {
                    regular: "#eb2727",
                    light: "#ffe6e6",
                },

            }
        },
        fontFamily : {
            body: ['Montserrat', 'sans-serif']
        },
        fontSize: {
            '3xl': ['2.5rem', {
                letterSpacing: '0',
                lineHeight: '3.25rem',
            }],
            // Or with a default line-height as well
            '2xl': ['2rem', {
                letterSpacing: '0',
                lineHeight: '2.563rem',
            }],
            'xl': ['1.5rem', {
                letterSpacing: '0',
                lineHeight: '1.938rem',
            }],
            'l': ['1.25rem', {
                letterSpacing: '0',
                lineHeight: '1.625rem',
            }],
            'm': ['1.125rem', {
                letterSpacing: '0',
                lineHeight: '1.75rem',
            }],
            's': ['1rem', {
                letterSpacing: '0',
                lineHeight: '1.625rem',
            }],
            'xs': ['0.875rem', {
                letterSpacing: '0',
                lineHeight: '1.375rem',
            }],

        },
        extend: {
            height: {
                xl: '80px',
                l: '60px',
                m: '40px',
                s: '20px',
                xs: '10px',
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
