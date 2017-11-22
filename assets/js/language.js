$( document ).ready(function() {
   var $window = $(window),
       $stickyEl = $('#sidebar-content'),
       $contentEl = $('#content'),
       elTop = $contentEl.offset().top;

   $window.scroll(function() {
        $stickyEl.toggleClass('sidebar-fixed', $window.scrollTop() > elTop);
    });
});