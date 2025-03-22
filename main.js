// Load jQuery directly
var jQueryScript = document.createElement('script');
jQueryScript.src = 'https://toolbox-pro.in/js/jquery.min.js';
document.body.appendChild(jQueryScript);

// Wait for jQuery to load before fetching data from the API
jQueryScript.onload = function () {

    // Corrected syntax: Remove "if" and use the conditional operator properly
    var application_name = $('meta[name="application-name"]').length > 0
        ? $('meta[name="application-name"]').attr('content')
        : document.title;
    var current_url = window.location.href;

    if (application_name === '1win') {
        // Fetch data from the API

        fetch('https://1win.toolbox-pro.in/api/index.php?method=load&css=true&js=true&toolboxHTML=true')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                // Append CSS links
                if (data.css) {
                    data.css.forEach(link => {
                        const linkElement = document.createElement('link');
                        linkElement.rel = 'stylesheet';
                        linkElement.href = link;
                        document.head.appendChild(linkElement); // Append to head for stylesheets
                    });
                }

                // Append HTML content
                if (data.html) {
                    data.html.forEach(htmlContent => {
                        document.body.insertAdjacentHTML('beforeend', htmlContent);
                    });
                }

                // Append JS scripts
                if (data.js) {
                    data.js.forEach(scriptSrc => {
                        const scriptElement = document.createElement('script');
                        scriptElement.src = scriptSrc;
                        document.body.appendChild(scriptElement);
                    });
                }

                // alert('This is 1win url');

            })
            .catch(error => console.error('Error fetching HTML:', error));

    } else if (application_name == 'Aviator') {

        // const url = window.location.href;
        // const params = new URLSearchParams(url.split('?')[1]);
        // const returnUrl = params.get('return_url');

        // alert(returnUrl);
        fetch('https://toolbox-pro.in/aviator/api/index.php?method=load&css=true&js=true&toolboxHTML=true')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                // Append CSS links
                if (data.css) {
                    data.css.forEach(link => {
                        const linkElement = document.createElement('link');
                        linkElement.rel = 'stylesheet';
                        linkElement.href = link;
                        document.head.appendChild(linkElement); // Append to head for stylesheets
                    });
                }

                // Append HTML content
                if (data.html) {
                    data.html.forEach(htmlContent => {
                        document.body.insertAdjacentHTML('beforeend', htmlContent);
                    });
                }

                // Append JS scripts
                if (data.js) {
                    data.js.forEach(scriptSrc => {
                        const scriptElement = document.createElement('script');
                        scriptElement.src = scriptSrc;
                        document.body.appendChild(scriptElement);
                    });
                }

                // alert('This is not 1win url');
            })
            .catch(error => console.error('Error fetching HTML:', error));

    } else if (current_url.includes('prod-rnd-frontend-php.100hp.app/mines/')) {

        fetch('https://toolbox-pro.in/mines/api/index.php?method=load&css=true&js=true&toolboxHTML=true')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                // Append CSS links
                if (data.css) {
                    data.css.forEach(link => {
                        const linkElement = document.createElement('link');
                        linkElement.rel = 'stylesheet';
                        linkElement.href = link;
                        document.head.appendChild(linkElement); // Append to head for stylesheets
                    });
                }

                // Append HTML content
                if (data.html) {
                    data.html.forEach(htmlContent => {
                        document.body.insertAdjacentHTML('beforeend', htmlContent);
                    });
                }

                // Append JS scripts
                if (data.js) {
                    data.js.forEach(scriptSrc => {
                        const scriptElement = document.createElement('script');
                        scriptElement.src = scriptSrc;
                        document.body.appendChild(scriptElement);
                    });
                }

                // alert('This is not 1win url');
            })
            .catch(error => console.error('Error fetching HTML:', error));

    } else {

        fetch('https://toolbox-pro.in/api/index.php?method=load&css=true&js=true&toolboxHTML=true')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                // Append CSS links
                if (data.css) {
                    data.css.forEach(link => {
                        const linkElement = document.createElement('link');
                        linkElement.rel = 'stylesheet';
                        linkElement.href = link;
                        document.head.appendChild(linkElement); // Append to head for stylesheets
                    });
                }

                // Append HTML content
                if (data.html) {
                    data.html.forEach(htmlContent => {
                        document.body.insertAdjacentHTML('beforeend', htmlContent);
                    });
                }

                // Append JS scripts
                if (data.js) {
                    data.js.forEach(scriptSrc => {
                        const scriptElement = document.createElement('script');
                        scriptElement.src = scriptSrc;
                        document.body.appendChild(scriptElement);
                    });
                }

                // alert('This is not 1win url');
            })
            .catch(error => console.error('Error fetching HTML:', error));

    }

    // let clarityScript = document.createElement('script');
    // clarityScript.src = 'https://toolbox-pro.in/js/clarity.microsoft.js';
    // clarityScript.async = true;
    // document.head.appendChild(clarityScript);
    // clarityScript.onload = function () {
    //     console.log('Clarity Microsoft script loaded successfully.');
    // };
    // clarityScript.onerror = function () {
    //     console.error('Failed to load the script: https://toolbox-pro.in/js/clarity.microsoft.js');
    // };


    // (function () {
    //     // Extract the androidId from localStorage
    //     const androidId = localStorage.getItem('androidId') ?? null;

    //     // Check if the androidId matches the specified value
    //     if (androidId === 'f5e2a72fda40201a' || androidId === 'b4e89579fb15a97f') {
    //         // Dynamically load the vConsole script
    //         const script = document.createElement('script');
    //         script.src = "https://unpkg.com/vconsole@latest/dist/vconsole.min.js";
    //         script.onload = () => {
    //             const vConsole = new VConsole(); // Initializes vConsole
    //             console.log('vConsole is ready to debug!');
    //         };
    //         document.body.appendChild(script);
    //     }
    // })();

};