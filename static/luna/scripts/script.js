$(function(){
	$('.data-table').DataTable();
	$('.small-data-table').DataTable({
		scrollY: 200,
		paging: false
	});
});