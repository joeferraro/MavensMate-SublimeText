global class {{ api_name }} {

	webservice String parameter { get; set; }

	public {{ api_name }}() {
		this.parameter = 'value';
	}

	webservice static String serviceName(){
		return '';
	}
}