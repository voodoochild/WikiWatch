/**
 * Watcher
 *
 * @author Kriss Watt <kriss.watt@gmail.com>
 * @version 1.0
 */
var Watcher = {};

/**
 * Watcher background module.
 *
 * @return {Object} Public methods.
 */
Watcher.background = function() {
    var visited_urls = [];
    
    /**
     * Checks the URL for the presence of a banned namespace.
     *
     * @private
     * @param {String} url The URL to test.
     * @return {Boolean} True if banned namespace is found in URL.
     */
    var containsBannedNamespace = function(url) {
        var pattern = '\/wiki\/(Wikipedia|Special|Help|File|Talk|' +
            'Portal|Template|Template_talk):.+',
            regex = new RegExp(pattern);
        matches = regex.exec(url);
        return matches && 0 < matches.length;
    };
    
    /**
     * Attempts to retrieve the upload_url from localStorage.
     *
     * @private
     * @return {String} The upload_url to use.
     */
    var getUploadUrl = function() {
        var url = localStorage['wikiwatch#upload_url'];
        if (!url || '' === url) {
            throw 'Watcher: no upload URL has been configured';
        }
        return url;
    };
    
    return {
        /**
         * If the URL points to wikipedia, it is logged to WikiWatch.
         *
         * @param {String} url The URL to log.
         */
        add: function(url) {
            var wpedia = url.indexOf('wikipedia.org'),
                wmedia = url.indexOf('wikimedia.org');
            if (-1 < wpedia || -1 < wmedia) {
                if (!containsBannedNamespace(url)) {
                    // TODO: this looks like it will break very easily
                    var matches = url.match(/(\/wiki\/.+)#.*$/);
                        url = (matches) ?
                            'http://en.wikipedia.org' + matches[1] : url;
                    
                    if (-1 === $.inArray(url, visited_urls)) {
                        visited_urls[visited_urls.length] = url;
                        $.get(getUploadUrl(), {
                            'url': url
                        }, function(data) {
                            console.log(data);
                        });
                    }
                }
            }
        },
        
        /**
         * Gets the URL from the current Chrome tab.
         */
        get: function() {
            chrome.windows.getCurrent(function(window) {
	            chrome.tabs.getSelected(window.id, function(tab) {
		            Watcher.background.add(tab.url);
	            });
	        });
        }
    };
}();


/**
 * Watcher options module.
 *
 * @return {Object} Public methods.
 */
Watcher.options = function() {
    var timeout;
    
    /**
     * Selectors for the available form fields.
     */
    var fields = [
        '#upload_url'
    ];
    
    /**
     * Form submit handler.
     *
     * @private
     * @param {Event} event The submit event.
     */
    var onSubmit = function(event) {
        var $this = $(event.target), i, $field;
        
        // TODO: add some kind of input sanitation
        for (i = 0; i < fields.length; i++) {
            $field = $this.find(fields[i]);
            if ($field) {
                localStorage['wikiwatch' + fields[i]] = $field.val();
            }
        }
        
        // TODO: add support for error messages
        var $confirmation = $this.find('span.confirmation');
        if ($confirmation) {
            clearTimeout(timeout);
            $confirmation.html('Your changes have been saved.').css({ 'opacity': 1 });
            timeout = setTimeout(function() {
                $confirmation.css({ 'opacity': 0 });
            }, 3000);
        }
        
        event.preventDefault();
    };
    
    return {
        /**
         * Adds a submit handler to the form and restore existing values.
         *
         * @param {String} selector
         */
        init: function(selector) {
            var $form = $(selector);
            
            if ($form) {
                $form.submit(onSubmit);
                Watcher.options.restore($form);
            }
        },
        
        /**
         * Attempts to restore the values of the options from localStorage.
         *
         * @param {Element} $form jQuery element representing the form.
         */
        restore: function($form) {
            var i, $field;
            
            for (i = 0; i < fields.length; i++) {
                $field = $form.find(fields[i]);
                
                if ($field) {
                    value = localStorage['wikiwatch' + fields[i]];
                    if ('undefined' !== typeof value) {
                        $field.val(value);
                    }
                }
            }
        }
    };
}();
