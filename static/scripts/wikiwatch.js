/**
 * WikiWatch
 *
 * @author Kriss Watt <kriss.watt@gmail.com>
 * @version 1.0
 */
var WikiWatch = {};

WikiWatch.expandCollapse = function() {
    /**
     * @param {Event} event
     */
    var onClick = function(event) {
        var $this = $(event.target);
        
        switch ($this.attr('mode')) {
            case 'closed':
                $this.parent('li').children('ul').show();
                $this.html('Less').attr('mode', 'open');
                break;
            default:
                $this.parent('li').children('ul').hide();
                $this.html('More').attr('mode', 'closed');
        }
        
        event.preventDefault();
    };
    
    return {
        init: function(selector) {
            $(selector).each(function() {
                $(this).click(onClick);
                $(this).trigger('click');
            });
        },
    };
}();

$(document).ready(function() {
    WikiWatch.expandCollapse.init('.expand');
});
