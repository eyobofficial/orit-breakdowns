$(function(){
    /**
    * Submit catagory selector form on change
    */
    $('.catagory-selector').change(function(){
        $('.cost-form').submit();
    });

    
    /**
    * Turn on/off between selecting an existing consultant and creating a new one
    * while creating a new project
    */
    $('input[name=consultant_option]').on('change', function(){
        if($(this).val() == '0'){
            $('#create-consultant-fieldset').prop('disabled', true);
            $('#select-consultant-fieldset').prop('disabled', false);
        }

        if($(this).val() == '1'){
            $('#create-consultant-fieldset').prop('disabled', false);
            $('#select-consultant-fieldset').prop('disabled', true);
        }
    });
});