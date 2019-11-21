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
    var checked_brand
    var checked_type
    var checked_gender
    var checked_size
    var checked_color
    var checked_price

    props_list.each(function(){
      var filter_type = $(this).attr('filter-type')
      if(this.checked){
        if(filter_type == "brand"){
          checked_brand = this.value;
        }
        if(filter_type == "type"){
          checked_type = this.value;
        }
        if(filter_type == "gender"){
          checked_gender = this.value;
        }
        if(filter_type == "size"){
          checked_size = this.value;
        }
        if(filter_type == "color"){
          checked_color = this.value
        }
        if(filter_type == "price"){
          checked_price = this.value
        }
      }
    });
    window.location.href = '/products/filter/?brandId=' + checked_brand + '&typeId=' + checked_type + '&genderId=' + checked_gender + '&sizeId=' + checked_size + '&colorId=' + checked_color + '&priceId=' + checked_price

  });

  // Kore Chatbot
  function assertion(options, callback) {
    var jsonData = {
      "clientId": botOptions.clientId,
      "clientSecret": botOptions.clientSecret,
      "identity": botOptions.userIdentity,
      "aud": "",
      "isAnonymous": true
    };
    $.ajax({
      url: botOptions.JWTUrl,
      type: 'post',
      data: jsonData,
      dataType: 'json',
      success: function (data) {
        options.assertion = data.jwt;
        options.handleError = koreBot.showError;
        options.chatHistory = koreBot.chatHistory;
        options.botDetails = koreBot.botDetails;
        callback(null, options);
        setTimeout(function () {
          if (koreBot && koreBot.initToken) {
            koreBot.initToken(options);
          }
        }, 2000);
      },
      error: function (err) {
        koreBot.showError(err.responseText);
      }
    });
  }

  var botOptions = {};
  botOptions.logLevel = 'debug';
  botOptions.koreAPIUrl = "https://bots.kore.ai/api/";
  botOptions.koreSpeechAPIUrl = "https://speech.kore.ai/";
  //botOptions.bearer = "bearer xyz-------------------";
  botOptions.ttsSocketUrl = 'wss://speech.kore.ai/tts/ws';
  botOptions.recorderWorkerPath = '../libs/recorderWorker.js';
  botOptions.assertionFn = assertion;
  botOptions.koreAnonymousFn = koreAnonymousFn;

  // To modify the web socket url use the following option
  // botOptions.reWriteSocketURL = {
          //     protocol: 'PROTOCOL_TO_BE_REWRITTEN',
          //     hostname: 'HOSTNAME_TO_BE_REWRITTEN',
          //     port: 'PORT_TO_BE_REWRITTEN'
          // };

  botOptions.JWTUrl ="https://demo.kore.net/users/sts";
  botOptions.userIdentity = 'huynguyen260398@gmail.com';// Provide users email id here
  botOptions.botInfo = {name:"Sneaky Virtual Assistant","_id":"st-2812988b-4560-57ca-ae27-f951d057d081"}; // bot name is case sensitive
  botOptions.clientId   = "cs-19ebb572-62b6-5d6c-93d6-81122c29b51c";
  botOptions.clientSecret="ahh/OJulIb7xaTdtXYGb2NmfxQY8TzqWQFmC283jf+o=";

  var chatConfig={
    botOptions:botOptions,
    allowIframe: false,
    isSendButton: false,
    isTTSEnabled: true,
    isSpeechEnabled: true,
    allowGoogleSpeech: false,
    allowLocation: true,
    loadHistory: false,
    messageHistoryLimit: 10,
    autoEnableSpeechAndTTS: false,
    graphLib: "d3",
    googleMapsAPIKey:"",
  };
  /*
    allowGoogleSpeech will use Google cloud service api.
    Google speech key is required for all browsers except chrome.
    On Windows 10, Microsoft Edge will support speech recognization.
   */
  var koreBot = koreBotChat();
  koreBot.show(chatConfig);
  $('.openChatWindow').click(function () {
    koreBot.show(chatConfig);
  });

  // Custom slide
  $('#carousel-example').on('slide.bs.carousel', function (e) {
      /*
          CC 2.0 License Iatek LLC 2018 - Attribution required
      */
      var $e = $(e.relatedTarget);
      var idx = $e.index();
      var itemsPerSlide = 5;
      var totalItems = $('.carousel-item').length;

      if (idx >= totalItems-(itemsPerSlide-1)) {
          var it = itemsPerSlide - (totalItems - idx);
          for (var i=0; i<it; i++) {
              // append slides to end
              if (e.direction=="left") {
                  $('.carousel-item').eq(i).appendTo('.carousel-inner');
              }
              else {
                  $('.carousel-item').eq(0).appendTo('.carousel-inner');
              }
          }
      }
  });

})
