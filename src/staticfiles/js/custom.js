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
  // $('.bo').change(function(){
      // var this = $(this)
      var billingForm = $('#my-billing-form')

      // if (this.value == 'different') {
      //   // billingForm.removeAttr('hidden')
      //   alert('different')
      // }

      switch($(this).val()) {
        case 'different' :
            // alert("different");
            billingForm.removeAttr('hidden');
            break;
        case 'same' :
            // alert("same");
            billingForm.attr('hidden', true);
            break;
      }

      // if (this.checked && this.value == 'different') {
      //   alert("different");
      //   billingForm.removeAttr('hidden')
      // } else {
      //   billingForm.addAttr('hidden')
      // }
  });

  // Filter Products by Properties
  $("input.my-filter").on('change', function () {
    event.preventDefault()
    // Loop all these checkboxes which are checked
    // $("input.my-filter:checked").each(function(){
    //     alert("it works");
    //     // Use $(this).val() to get the Bike, Car etc.. value
    // });
    var props_list = $("input.my-filter");
    // var checked_props = [];

    var brand
    var checked_brand
    var type
    var checked_type
    var size
    var checked_size
    var color
    var checked_color

    // var checked_prop

    // if(this.checked){
    //   alert("checked - " + this.value);
    // } else {
    //   alert("unchecked - " + prop);
    // }

    props_list.each(function(){
      var filter_type = $(this).attr('filter-type')
      if(this.checked){
        // checked_props.push(this.value);
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
        // checked_prop = this.value;
      }
    });


    // sendFilterBag("brand", checked_props)

    // window.location.href = '/products/?brand=' + checked_props[0]
    window.location.href = '/products/filter/?brandId=' + checked_brand + '&typeId=' + checked_type + '&sizeId=' + checked_size + '&colorId=' + checked_color

  });

  // by TYPE
  // $("input.my-filter-type").on('change', function () {
  //   event.preventDefault()
  //   var props_list = $("input.my-filter-brand");
  //   var checked_type;
  //
  //   props_list.each(function(){
  //     if(this.checked){
  //       checked_type = this.value;
  //     }
  //   });
  //
  //   window.location.href = '/products/?brand=' + checked_props[0]
  //
  // });

  function sendFilterBag(props_type, props){
    console.log(props_type)
    console.log(props)

    $.ajax({
      url: '/products/',
      method: "GET",
      data: {
        props_type: props_type,
        props: props,
      },
      // dataType: 'json',
      success: function(data){
        // console.log(data.selected)
        console.log("filtered")
      },
      error: function(error){
        console.log("unfiltered")
      }
    })
  }

})
