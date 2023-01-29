// variables


const cardBtn = document.querySelector('.icon-search');
const modalActive = document.querySelector('.modal');
const close = document.querySelector('.close');




cardBtn.addEventListener('click',() => {
    modalActive.style.display = 'block' ;
})

close.addEventListener('click', () => {
    modalActive.style.display = 'none';
})


// ------------ img -------- >>>

const productImg = document.querySelector('#product-img');
const subImg = document.querySelectorAll('.sub-img');



subImg.forEach(item => {
    item.addEventListener('click',() => {
        productImg.src = item.src;
    })
})


// subImg[0].onclick = function(){
//     productImg.src = subImg[0].src;
// }



