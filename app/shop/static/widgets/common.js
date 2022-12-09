document.addEventListener('DOMContentLoaded', function(){
    const money_masks = document.querySelectorAll('input[type=text][data-mask-money=on]');
    for (let i = 0; i < money_masks.length; i += 1) {
        VMasker(money_masks[i]).maskMoney({
            precision: 2,
            separator: '.',
            delimiter: ' ',
        });
    }
});
