$(document).ready(function () {
    url_pdf = $('#url_pdf').val()
    $("#flip_book").flipBook({
        pdfUrl: url_pdf,
        viewMode:'3d',
        skin:'white',
        // Иконки панели — Material Icons (Font Awesome на сайте больше не подключается)
        icons: 'material',
        assets: {
            preloader: '/static/libs/flipbook/images/preloader.jpg',
            overlay: '/static/libs/flipbook/images/overlay.png',
            flipMp3: '/static/sounds/turnPage.mp3',
            spinner: '/static/images/more/spinner.gif'
        },
        btnSearch: {
            enabled: true,
            title: "Поиск"
        },
        btnSound : {enabled:false},
        btnAutoplay : {enabled:false},
        btnShare : {enabled:false},
        btnBookmark : {enabled:false},
        btnPrint : {enabled:false},
        btnDownloadPages : {enabled:false},
        btnDownloadPdf : {enabled:false},
    });
    $('#url_pdf').remove()
})