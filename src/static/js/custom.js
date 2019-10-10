$(document).ready(function(){
  // Contact Form Handler
  var contactForm = $('.my-contact-form')
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
      $.confirm({
          title: 'Oops!',
          content: 'Please choose your size!',
          type: 'orange',
          typeAnimated: true,
          buttons: {
              tryAgain: {
                  text: 'OK',
                  btnClass: 'btn-orange',
                  action: function(){
                  }
              }
          }
      });
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
          // alert('success')
          $.confirm({
              title: 'Success!',
              content: 'Item added to your bag!',
              type: 'green',
              typeAnimated: true,
              buttons: {
                  tryAgain: {
                      text: 'Continue Shopping',
                      btnClass: 'btn-green',
                      action: function(){
                      }
                  }
              }
          });
        },
        error: function(error){
          alert(error)
        }
      })
    }
  });

  // Billing Option
  $('input:radio[name="billing_option"]').change(function(){
      var billingForm = $('#my-billing-form')

      switch($(this).val()) {
        case 'different' :
            billingForm.removeAttr('hidden');
            break;
        case 'same' :
            billingForm.attr('hidden', true);
            break;
      }
  });

  // Filter Products by Properties
  $("input.my-filter").on('change', function () {
    event.preventDefault()
    var props_list = $("input.my-filter");
    var brand
    var checked_brand
    var type
    var checked_type
    var size
    var checked_size
    var color
    var checked_color

    props_list.each(function(){
      var filter_type = $(this).attr('filter-type')
      if(this.checked){
        if(filter_type == "brand"){
          checked_brand = this.value;
        }
        if(filter_type == "type"){
          checked_type = this.value;
        }
        if(filter_type == "size"){
          checked_size = this.value;
        }
        if(filter_type == "color"){
          checked_color = this.value
        }
      }
    });
    window.location.href = '/products/filter/?brandId=' + checked_brand + '&typeId=' + checked_type + '&sizeId=' + checked_size + '&colorId=' + checked_color

  });
})
