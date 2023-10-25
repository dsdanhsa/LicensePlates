function success(mess) {
	toastr.options.showMethod = 'slideDown';
	toastr.options.hideMethod = 'slideUp';
	toastr.options.closeMethod = 'slideUp';
	toastr.options.timeOut = 3000;
	
	toastr.success(mess,'Thông báo');
}
function warning(mess) {
	toastr.options.showMethod = 'slideDown';
	toastr.options.hideMethod = 'slideUp';
	toastr.options.closeMethod = 'slideUp';
	toastr.options.timeOut = 3000;
	
	toastr.warning(mess,'Thông báo');
}
function error(mess) {
	toastr.options.showMethod = 'slideDown';
	toastr.options.hideMethod = 'slideUp';
	toastr.options.closeMethod = 'slideUp';
	toastr.options.timeOut = 3000;
	toastr.error(mess,'Thông báo');
}