//function serialize(form){if(!form||form.nodeName!=="FORM"){return }var i,j,q=[];for(i=form.elements.length-1;i>=0;i=i-1){if(form.elements[i].name===""){continue}switch(form.elements[i].nodeName){case"INPUT":switch(form.elements[i].type){case"text":case"hidden":case"password":case"button":case"reset":case"submit":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"checkbox":case"radio":if(form.elements[i].checked){q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value))}break;case"file":break}break;case"TEXTAREA":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"SELECT":switch(form.elements[i].type){case"select-one":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"select-multiple":for(j=form.elements[i].options.length-1;j>=0;j=j-1){if(form.elements[i].options[j].selected){q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].options[j].value))}}break}break;case"BUTTON":switch(form.elements[i].type){case"reset":case"submit":case"button":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break}break}}return q.join("&")};
function capFirst(str) { var newStr = str.toLowerCase(); return newStr[0].toUpperCase() + newStr.substr(1); }
function formatBRL(str) { return str.toFixed(2).replace('.', ','); }

var PagSeguro = function(opts) {
    var defaultOptions = {
        installments: true,
        amount: 600,
        maxInstallmentNoInterest: 3,
    };
    var options = Object.assign({}, defaultOptions, opts);

    function formSubmit(e) {
        if (options.submited) {
            return;
        }
        options.submited = true;
        e.preventDefault();

        PagSeguroDirectPayment.createCardToken({
            cardNumber: document.getElementById('credit_card_num').value.replace(' ', ''),
            brand: document.getElementById('credit_card_brand').value,
            cvv: document.getElementById('credit_card_cvv').value,
            expirationMonth: document.getElementById('credit_card_month').value,
            expirationYear: document.getElementById('credit_card_year').value,
            success: function(response) {
                document.getElementById('credit_card_token').value = response.card.token;
                getSenderHashKey();
            },
            error: function(response) {
            },
            complete: function(response) {
            }
        });
    }

    function bindForm() {
        document.getElementById('payment_form').addEventListener('submit', formSubmit);
    }

    function getSenderHashKey() {
        PagSeguroDirectPayment.onSenderHashReady(function(response){
            if(response.status == 'error') {
                console.log(response.message);
                return false;
            }
            document.getElementById('user_hash_token').value = response.senderHash;
            // var form = document.getElementById('payment_form');
            // var data = serialize(form);
            var installment = document.querySelector('input[name=installment]:checked');
            if (!installment) {
                document.getElementById('error-message').innerHTML = 'Houve um erro desconhecido e não conseguimos encontrar a forma como deseja pagar.';
                return;
            }
            document.getElementById('payment_form').submit();
            /*
            var checkoutData = {
                senderHash: response.senderHash,
                creditCardToken: document.getElementById('credit_card_token').value,
                installmentQuantity: installment.getAttribute('data-quantity'),
                installmentValue: installment.value,
            };
            var req = new XMLHttpRequest();
            req.onload = function(e) {
                console.log(req.responseText);
            }
            req.open('POST', options.finishUrl);
            req.setRequestHeader('Content-Type', 'application/json');
            // console.log(checkoutData);
            req.send(JSON.stringify(checkoutData));
            */
        });
    }

    function getInstallments(brand) {
        PagSeguroDirectPayment.getInstallments({
            amount: options.amount,
            maxInstallmentNoInterest: options.maxInstallmentNoInterest,
            brand: brand,
            success: function(response){
                var installments = response.installments[brand];
                var html = '';
                for (var i = 0; i < installments.length; i += 1) {
                    var obj = installments[i];
                    var quantity = obj.quantity;
                    var interestFree = obj.interestFree;
                    var installmentAmount = obj.installmentAmount;
                    var totalAmount = obj.totalAmount;
                    html += '<p><label>';
                    html += '<input name="installment" id="installment_opt_' + quantity + '" type="radio" data-quantity="' + quantity + '" ' + (quantity === 1 ? 'checked="checked" ' : '') + ' value="' + installmentAmount + '" />';
                    html += '<span>' + quantity + ' parcelas ' + (interestFree ? 'sem juros ' : '') + '   de R$ ' + formatBRL(installmentAmount) + ' (R$ ' + formatBRL(totalAmount) + ')' + '</span>';
                    html += '</p></label>';
                }
                document.getElementById('installments').innerHTML = html;
            },
            error: function(response) {
            },
            complete: function(response){
            }
        });
    }

    function creditCardNumberKeyUp(e) {
        var cardNum = e.target.value.replace(' ', '');
        if (cardNum.length < 6) {
            document.getElementById('credit_card_num_brand').innerHTML = '';
            document.getElementById('error-message').innerHTML = '';
            document.getElementById('installments').innerHTML = '';
            document.getElementById('credit_card_brand').value = '';
            return;
        }
        PagSeguroDirectPayment.getBrand({
            cardBin: cardNum,
            success: function(response) {
                document.getElementById('credit_card_num_brand').innerHTML = capFirst(response.brand.name);
                document.getElementById('error-message').innerHTML = '';
                document.getElementById('credit_card_brand').value = response.brand.name;
                document.getElementById('credit_card_cvv').setAttribute('maxlength', response.brand.cvvSize);
                if (options.installments) {
                    getInstallments(response.brand.name);
                } else {
                    document.getElementById('installments').innerHTML = '';
                }
            },
            error: function(response) {
                document.getElementById('installments').innerHTML = '';
                document.getElementById('credit_card_num_brand').innerHTML = '';
                document.getElementById('credit_card_brand').value = '';
                document.getElementById('error-message').innerHTML = 'Cartão Inválido';
            },
            complete: function(response) {
            }
        });        
    }

    function creditCardBinds() {
        document.getElementById('credit_card_num').addEventListener('keyup', creditCardNumberKeyUp);
    };

    function populatePaymentMethods() {
        PagSeguroDirectPayment.getPaymentMethods({
            amount: options.amount,
            success: function(response) {
                if (response.error) {
                    return;
                }
                var relPath = 'https://stc.pagseguro.uol.com.br';
                var credit_cards = response.paymentMethods.CREDIT_CARD.options;
                var keys = Object.keys(credit_cards);
                var html = '';
                for (var i = 0; i < keys.length; i += 1) {
                    var obj = credit_cards[keys[i]];
                    html += 
                        '<div class="payment-method-brand">' +
                        '   <img src="' + relPath + obj.images.SMALL.path + '" />' +
                        '   <span>' + capFirst(obj.name) + '</span>' +
                        '</div>';
                }
                document.getElementById('credit-card').innerHTML = html;
                document.getElementById('boleto').innerHTML +=
                    '<div class="payment-method-brand">' +
                    '   <img src="' + relPath + response.paymentMethods.BOLETO.options.BOLETO.images.SMALL.path + '" />' +
                    '   <span>Boleto</span>'
                    '</div>';
                creditCardBinds();
                document.getElementById('loading-box').style.display = 'none';
            },
            error: function(response) {
            },
            complete: function(response) {
                bindForm();
            }
        });        
    }

    function auth(authUrl) {
        var req = new XMLHttpRequest();
        req.onload = function() {
            if (req.status === 200) {
                const id = JSON.parse(req.responseText).id;
                PagSeguroDirectPayment.setSessionId(id);
                populatePaymentMethods();
            }
        }
        req.open('GET', authUrl);
        req.send();
    }

    if (opts.url == null || opts.url == undefined) {
        return;
    }
    auth(opts.url);
};

