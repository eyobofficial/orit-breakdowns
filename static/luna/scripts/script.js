$(function(){
	$('.data-table').DataTable();
	$('.small-data-table').DataTable({
		scrollY: 200,
		paging: false
	});

	$('a[target="_blank"]').append(' &nbsp;<small><i class="fa fa-external-link"></i></small>');

	$(document).ready(function(){
	  $('#adapt-breakdown-wizard').smartWizard();
	});
});