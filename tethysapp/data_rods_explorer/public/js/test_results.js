/**
 * Created by alan on 12/17/16.
 */
function checkTests() {
    $.ajax({
        url: '/apps/data-rods-explorer/run-tests',
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response.hasOwnProperty('results')) {
                $('#progressTotal').css('width', '100%');
                $('#progressText').text('100%');
                $('#header').addClass('hidden');
                $('#results').html(response.results);
                var failedUrls = JSON.parse(response.failed_urls.replace(/&quot;/g, '"'));
                var failedUrlHTML = '';
                failedUrls.forEach(function (url) {
                    failedUrlHTML += '<br><a href="' + url + '" target="_blank">' + url + '</a>';
                });
                $('#failedUrls').html(failedUrlHTML);
            } else if (response.hasOwnProperty('counter')) {
                var counter = Number(response.counter);
                var total = Number(response.total_endpoints);
                var percent = Math.floor(100 * counter / total);
                $('#progressTotal').css('width', percent + '%');
                $('#progressText').text(percent + '%');
                window.setTimeout(function () {
                    checkTests();
                }, 2000)
            }
        }
    });
}
$(function () {
    checkTests()
});