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
  var productForm = $('.form-product-ajax')

  function getOwnedProduct(productId, submitSpan){
    var actionEndpoint = '/orders/endpoint/verify/ownership/'
    var httpMethod = 'GET'
    var data = {
      product_id: productId
    }

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: data,
      success: function(data){
        console.log(data)
        if (data.owner){
          submitSpan.html("<a class='btn btn-warning' href='/library/'>In Library</a>")
        }
      },
      error: function(error){
        console.log(error)
      }
    })
  }

  $.each(productForm, function(index, object){
    var $this = $(this)
    var isUser = $this.attr('data-user')
    var submitSpan = $this.find('.submit-span')
    var productInput = $this.find("[name='product_id']")
    var productId = productInput.attr('value')
    var productIsDigital = productInput.attr('data-is-digital')

    if (productIsDigital && isUser){
      var isOwned = getOwnedProduct(productId, submitSpan)
    }
  })

  productForm.submit(function(event){
    event.preventDefault()
    var thisForm = $(this)
    var actionEndpoint = thisForm.attr('data-endpoint')
    var httpMethod = thisForm.attr('method')
    var formData = thisForm.serialize()

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-span")
        var navbarCount = $(".navbar-cart-count")

        if (data.added){
          submitSpan.html("<div class='btn-group'><a class='btn btn-danger' href='/cart/'>In cart </a><button type='submit' class='btn btn-danger'><i class='fas fa-trash'></i> Remove</button></div>")
          navbarCount.html("<i class='fas fa-shopping-cart'></i> (" + data.cartItemCount + ")")
        } else {
          submitSpan.html("<button type='submit' class='btn btn-success'><i class='fas fa-cart-plus'></i> Add to cart</button>")
          if (data.cartItemCount > 0){
            navbarCount.html("<i class='fas fa-shopping-cart'></i> (" + data.cartItemCount + ")")
          } else {
            navbarCount.html("<i class='fas fa-shopping-cart'></i> ")
          }
        }

        var currentPath = window.location.href
        if (currentPath.indexOf('cart') != -1){
          refreshCart()
        }
      },
      error: function(data){
        $.alert({
          title: "Oops!",
          content: "An error has occurred!",
          theme: "modern",
        })
      }
    })
  })

  function refreshCart(){
    var cartTable = $('.cart-table')
    var cartBody = cartTable.find('.cart-body')
    var productRows = cartBody.find('.cart-product')
    var currentUrl = window.location.href

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = 'GET'

    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: {},
      success: function(data){
        console.log(data)
        var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
        if (data.products.length > 0){
          productRows.html(" ")
          i = data.products.length
          $.each(data.products, function(index, value){
            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            newCartItemRemove.css('display', 'block')
            newCartItemRemove.find('.cart-item-product-id').val(value.id)
            cartBody.prepend("<tr><th scope='row'>" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a></td><td><i class='fas fa-dollar-sign'></i> " + value.price + "</td><td>" + newCartItemRemove.html() + "</td></tr>")
            i--
          })
          cartBody.find('.cart-subtotal').text(data.subtotal)
          cartBody.find('.cart-total').text(data.total)
        } else {
          window.location.href = currentUrl
        }
      },
      error: function(errorData){
        $.alert({
          title: "Oops!",
          content: "An error has occurred!",
          theme: "modern",
        })
      }
    })
  }
})
