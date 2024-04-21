(function () {
    const sliderBox = document.querySelector('.el-kitep-book-slider .swiper-wrapper');
    fetch('https://www.ebs.el-kitep.kg/api/v1/books/api_0a647bddffa3058a302b5b20c9b33612/').then(
        response => response.json()
    ).then(result => {
        result.data.forEach(book => {
            const image = `<img src="${book.thumbnail}" alt="${book.title}"/>`
            const link = `<a href="${book.url}" target="_blank" class="swiper-slide">${image}</a>`
            sliderBox.insertAdjacentHTML("afterbegin", link)
        })
        new Swiper(".el-kitep-book-slider", {
            effect: "cards",
            grabCursor: true,
            autoplay: {
                delay: 2300, // Delay between slides in milliseconds
                disableOnInteraction: false, // Disable autoplay on user interaction
            },
            spaceBetween: 50,
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
    })
})()
