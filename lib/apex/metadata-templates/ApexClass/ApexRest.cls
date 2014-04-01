@RestResource(urlMapping='/YourCustomResource')
global with sharing class {{ api_name }} {

    @HttpPost  
      global static void doPost(){

      }

    @HttpPut 
      global static void doPut(){

      }

    @HttpGet
      global static void doGet(){

      }

    @HttpDelete
      global static void doDelete(){

      }
}