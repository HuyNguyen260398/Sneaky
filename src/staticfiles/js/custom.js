$(document).ready(function(){
  // Contact Form Handler
  var contactForm = $('.contact-form')
  var contactFormMethod = contactForm.attr('method')
  var contactFormEndpoint = contactForm.attr('action')

  function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html('<i class="fas fa-circle-notch fa-spin"></i>')
    } else {
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }

  }

  contactForm.submit(function(event){
    event.preventDefault()
    var contactFormData = contactForm.serialize()
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnText = contactFormSubmitBtn.text()
    displaySubmitting(contactFormSubmitBtn, "", true)

    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data){
        contactForm[0].reset()
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "modern",
        })
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnText, false)
        }, 500)
      },
      error: function(error){
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""
        $.each(jsonData, function(key, value){
          msg += key + ": " + value[0].message + "<br/>"
        })
        $.alert({
          title: "Oops!",
          content: msg,
          theme: "modern",
        })
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnText, false)
        }, 500)
      }
    })
  })

  // Auto Search
  var searchForm = $('.search-form')
  var searchInput = searchForm.find("[name='q']")
  var typingTimer
  var typingInterval = 1000 // in miliseconds
  var searchBtn = searchForm.find("[type='submit']")

  searchInput.keyup(function(event){
    // key released
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)
  })

  searchInput.keydown(function(event){
    // key pressed
    clearTimeout(typingTimer)
  })

  function searchLoading(){
    searchBtn.addClass('disabled')
    searchBtn.html('<i class="fas fa-circle-notch fa-spin"></i>')
  }

  function performSearch(){
    searchLoading()
    var query = searchInput.val()
    setTimeout(function(){
      window.location.href = '/search/?q=' + query
    }, 500)
  }

  // Cart + Add Products

  $('#add-cart-btn').click(function(event){

    event.preventDefault()
    var actionEndpoint = $(this).attr('data-endpoint')
    var productId = $(this).attr('data-product')
    var colorId = $(this).attr('data-color')
    var sizeId = $('input[name=product-size]:checked').val()

    if(!sizeId){
      alert('please choose a size')
    }else{
      // alert(productId + " " + colorId + " " + sizeId)
      $.ajax({
        url: actionEndpoint,
        method: "POST",
        data: {
          product_id: productId,
          color_id: colorId,
          size_id: sizeId,
        },
        success: function(data){
          var navbarCount = $(".navbar-cart-count")
          navbarCount.html("<i class='fas fa-shopping-bag'></i> [" + data.cartItemCount + "]")
          alert('success')
        },
        error: function(error){
          alert(error)
        }
      })
    }
  })

//   function refreshCart(){
//     var cartTable = $('.cart-table')
//     var cartBody = cartTable.find('.cart-body')
//     var productRows = cartBody.find('.cart-product')
//     var currentUrl = window.location.href
//
//     var refreshCartUrl = '/api/cart/'
//     var refreshCartMethod = 'GET'
//
//     $.ajax({
//       url: refreshCartUrl,
//       method: refreshCartMethod,
//       data: {},
//       success: function(data){
//         console.log(data)
//         var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
//         if (data.products.length > 0){
//           productRows.html(" ")
//           i = data.products.length
//           $.each(data.products, function(index, value){
//             var newCartItemRemove = hiddenCartItemRemoveForm.clone()
//             newCartItemRemove.css('display', 'block')
//             newCartItemRemove.find('.cart-item-product-id').val(value.id)
//
//             itemIndex = "<tr><th scope='row'>" + i + "</th>"
//             itemRemove = "<td class='product-remove'>" + newCartItemRemove.html() + "</td>"
//             itemImage = "<td class='image-prod'><div class='img' style='background-image:url(" +  value.image + ");'></div></td>"
//             itemName = "<td class='product-name'><h3>" + value.name + "</h3></td>"
//             itemPrice = "<td class='price'>$" + value.price + "</td>"
//             itemQuantity = "<td class='quantity'><div class='input-group mb-3'><input type='text' name='quantity' class='quantity form-control input-number' value='1' min='1' max='100'></div></td>"
//             itemTotal = "<td class='total'>$4.90</td></tr>"
//
//             cartBody.prepend(itemIndex, itemRemove, itemImage, itemName, itemPrice, itemQuantity, itemTotal)
//             i--
//           })
//           cartBody.find('.cart-subtotal').text(data.subtotal)
//           cartBody.find('.cart-total').text(data.total)
//         } else {
//           window.location.href = currentUrl
//         }
//       },
//       error: function(errorData){
//         $.alert({
//           title: "Oops!!!!",
//           content: errorData,
//           theme: "modern",
//         })
//       }
//     })
//   }
})
