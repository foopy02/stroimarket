var modal = document.getElementById("myModal");

var btn = document.getElementById("myBtn");

var span = document.getElementsByClassName("close")[0];

var input = document.getElementById('myInput');
var message = document.getElementById('myUL');


// FOR DEMO PURPOSE ONLY
// =====================
// var demoForm  = document.querySelector('.demoForm');
// demoForm.addEventListener("onclick", function(e) {
//   e.preventDefault();
// }, true);


$("#myInput").focusin(function() {
  $("#myUL").show();
})

window.addEventListener("click", function(event) {
  if (event.target.className != "list_item" && event.target.id != "myInput" ){
    message.style.display = 'none';
  var demoInput = document.querySelector('input[name="rate"]:checked');

      if (!demoInput) {
    console.log('пуста капуста...');
  } else {
    console.log(demoInput.value); 
    var star_input = this.document.getElementById("stars")
    star_input.setAttribute('value', demoInput.value)
  }
  }
});

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var number_of_product = document.getElementById("number_of_product")

function increment(){
    number_of_product.value++
}

function decrement(){
    number_of_product.value--
}


var owl = $('.owl-carousel');
owl.owlCarousel({
    items:1,
    loop:true,
    margin:10,
    autoplay:true,
    autoplayTimeout:5000,
    autoplayHoverPause:true
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[5000])
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
})


function sort(){
  let nav = document.querySelector('#products')
  for(let i = 0; i < nav.children.length; i++){
    for (let j = i; j < nav.children.length; j++){
      if(+nav.children[i].getAttribute('data-sort') > +nav.children[j].getAttribute('data-sort')){
        replacedNode = nav.replaceChild(nav.children[j], nav.children[i])
        insertAfter(replacedNode, nav.children[i]);
      }
    }
  }
}

function descSort(){
  let nav = document.querySelector('#products')
  for(let i = 0; i < nav.children.length; i++){
    for (let j = i; j < nav.children.length; j++){
      if(+nav.children[i].getAttribute('data-sort') < +nav.children[j].getAttribute('data-sort')){
        replacedNode = nav.replaceChild(nav.children[j], nav.children[i])
        insertAfter(replacedNode, nav.children[i]);
      }
    }
  }
}

function sortAtoZ(){
  let nav = document.querySelector('#products')
  for(let i = 0; i < nav.children.length; i++){
    for (let j = i; j < nav.children.length; j++){
      if(nav.children[i].getAttribute('data-title') > nav.children[j].getAttribute('data-title')){
        replacedNode = nav.replaceChild(nav.children[j], nav.children[i])
        insertAfter(replacedNode, nav.children[i]);
      }
    }
  }
}

function sortZtoA(){
  let nav = document.querySelector('#products')
  for(let i = 0; i < nav.children.length; i++){
    for (let j = i; j < nav.children.length; j++){
      if(nav.children[i].getAttribute('data-title') < nav.children[j].getAttribute('data-title')){
        replacedNode = nav.replaceChild(nav.children[j], nav.children[i])
        insertAfter(replacedNode, nav.children[i]);
      }
    }
  }
}

function insertAfter(elem, refElem){
  return refElem.parentNode.insertBefore(elem, refElem.nextSibling);
}

// // Ajax for creating short alert
function to_cart(product){
  product_id = product.getAttribute('data-id')
  counter = document.getElementById('amount_of_items_in_cart')
  counter.textContent = +counter.textContent + 1 
  $.ajax({
      type: 'GET',
      url: "/user/add_to_cart/",
      data: {
        id:product_id
      },
      success: function(response){
        product.innerHTML = "<span style='color: green; font-size: 25px'>✓</span>"
      },
      error: function(xhr, ajaxOptions, thrownError){

      }
  });
}

function to_cart_with_amount(product){
  product_id = product.getAttribute('data-id')
  amount = document.getElementById('number_of_product').value
  counter = document.getElementById('amount_of_items_in_cart')
  counter.textContent = +counter.textContent + +amount 
  $.ajax({
      type: 'GET',
      url: "/user/add_to_cart_with_amount/",
      data: {
        id:product_id,
        amount:amount
      },
      success: function(response){
        
      },
      error: function(xhr, ajaxOptions, thrownError){

      }
  });
}

function delete_product(product){
  console.log(product)

  product_id = product.getAttribute('data-id')
  console.log(product_id)

  // counter.textContent = +counter.textContent - 1 
  $.ajax({
      type: 'GET',
      url: "/cart/delete/",
      data: {
        id:product_id
      },
      success: function(response){
        
      },
      error: function(xhr, ajaxOptions, thrownError){
        alert(xhr.status);
      }
  });
}

function myFunction() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

