$(document).ready(function(){
    $('.softkeys').softkeys({
        target : $('.softkeys').data('target'),
        layout : [
            [
                '1','2','3'
            ],
            [
                '4','5','6'
            ],
            [
                '7','8','9'
            ],
            [
                '0','delete'
            ]
        ]
    });
});