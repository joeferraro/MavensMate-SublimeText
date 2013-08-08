{
  "publicDeclarations" : {
    "Apex" : {
      "EmptyStackException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EmptyStackException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "Exception"
          } ],
          "name" : "EmptyStackException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          } ],
          "name" : "EmptyStackException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          }, {
            "name" : "param2",
            "type" : "Exception"
          } ],
          "name" : "EmptyStackException",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Stack" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Stack",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "empty",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "peek",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "pop",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "item",
            "type" : "String"
          } ],
          "name" : "push",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "ApexPages" : {
      "Action" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "expression",
            "type" : "String"
          } ],
          "name" : "Action",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getExpression",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "invoke",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Component" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ApexPages.Component",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "String"
          } ],
          "name" : "getComponentById",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "childComponents",
          "references" : [ ]
        }, {
          "name" : "componentIterations",
          "references" : [ ]
        }, {
          "name" : "expressions",
          "references" : [ ]
        }, {
          "name" : "facets",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "parent",
          "references" : [ ]
        }, {
          "name" : "rendered",
          "references" : [ ]
        } ]
      },
      "ComponentIteration" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ApexPages.Component",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "String"
          } ],
          "name" : "getComponentById",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "childComponents",
          "references" : [ ]
        }, {
          "name" : "iterationValue",
          "references" : [ ]
        }, {
          "name" : "parent",
          "references" : [ ]
        } ]
      },
      "IdeaStandardController" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "fieldNames",
            "type" : "LIST<String>"
          } ],
          "name" : "addFields",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "cancel",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "edit",
          "references" : [ ]
        }, {
          "returnType" : "LIST<IdeaComment>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCommentList",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getId",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecord",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSubject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "save",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "view",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "IdeaStandardSetController" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "fieldNames",
            "type" : "LIST<String>"
          } ],
          "name" : "addFields",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "cancel",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "first",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCompleteResult",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getFilterId",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHasNext",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHasPrevious",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Idea>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getIdeaList",
          "references" : [ ]
        }, {
          "returnType" : "LIST<System.SelectOption>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getListViewOptions",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPageNumber",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPageSize",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecord",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecords",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getResultSize",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSelected",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "last",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "previous",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "save",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "filterId",
            "type" : "String"
          } ],
          "name" : "setFilterId",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "pageNumber",
            "type" : "Integer"
          } ],
          "name" : "setPageNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "setPageSize",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "selected",
            "type" : "LIST<SObject>"
          } ],
          "name" : "setSelected",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "KnowledgeArticleVersionStandardController" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "fieldNames",
            "type" : "LIST<String>"
          } ],
          "name" : "addFields",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "cancel",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "edit",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getId",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecord",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSourceId",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSubject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "save",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "categoryGroup",
            "type" : "String"
          }, {
            "name" : "category",
            "type" : "String"
          } ],
          "name" : "selectDataCategory",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "view",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Message" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getComponentLabel",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDetail",
          "references" : [ ]
        }, {
          "returnType" : "ApexPages.Severity",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSeverity",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSummary",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Severity" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ApexPages.Severity>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "CONFIRM",
          "references" : [ ]
        }, {
          "name" : "ERROR",
          "references" : [ ]
        }, {
          "name" : "FATAL",
          "references" : [ ]
        }, {
          "name" : "INFO",
          "references" : [ ]
        }, {
          "name" : "WARNING",
          "references" : [ ]
        } ]
      },
      "StandardController" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "fieldNames",
            "type" : "LIST<String>"
          } ],
          "name" : "addFields",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "cancel",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "edit",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getId",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecord",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSubject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "save",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "view",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "StandardSetController" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "fieldNames",
            "type" : "LIST<String>"
          } ],
          "name" : "addFields",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "cancel",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "first",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCompleteResult",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getFilterId",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHasNext",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHasPrevious",
          "references" : [ ]
        }, {
          "returnType" : "LIST<System.SelectOption>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getListViewOptions",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPageNumber",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPageSize",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecord",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRecords",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getResultSize",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSelected",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "last",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "previous",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "save",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "filterId",
            "type" : "String"
          } ],
          "name" : "setFilterId",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "pageNumber",
            "type" : "Integer"
          } ],
          "name" : "setPageNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "setPageSize",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "selected",
            "type" : "LIST<SObject>"
          } ],
          "name" : "setSelected",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "ConnectApi" : {
      "AbstractMessageBody" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "messageSegments",
          "references" : [ ]
        }, {
          "name" : "text",
          "references" : [ ]
        } ]
      },
      "Actor" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        } ]
      },
      "ActorWithId" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "motif",
          "references" : [ ]
        }, {
          "name" : "mySubscription",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "Address" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Address",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "city",
          "references" : [ ]
        }, {
          "name" : "country",
          "references" : [ ]
        }, {
          "name" : "formattedAddress",
          "references" : [ ]
        }, {
          "name" : "state",
          "references" : [ ]
        }, {
          "name" : "street",
          "references" : [ ]
        }, {
          "name" : "zip",
          "references" : [ ]
        } ]
      },
      "ApprovalAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ApprovalAttachment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "postTemplateFields",
          "references" : [ ]
        }, {
          "name" : "status",
          "references" : [ ]
        } ]
      },
      "ApprovalPostTemplateField" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ApprovalPostTemplateField",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "displayName",
          "references" : [ ]
        }, {
          "name" : "displayValue",
          "references" : [ ]
        }, {
          "name" : "record",
          "references" : [ ]
        } ]
      },
      "BasicTemplateAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "BasicTemplateAttachment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "icon",
          "references" : [ ]
        }, {
          "name" : "linkRecordId",
          "references" : [ ]
        }, {
          "name" : "linkUrl",
          "references" : [ ]
        }, {
          "name" : "subtype",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        } ]
      },
      "BinaryInput" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "blobValue",
            "type" : "Blob"
          }, {
            "name" : "contentType",
            "type" : "String"
          }, {
            "name" : "filename",
            "type" : "String"
          } ],
          "name" : "BinaryInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBlobValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getContentType",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getFilename",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "CaseActorType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.CaseActorType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Customer",
          "references" : [ ]
        }, {
          "name" : "CustomerService",
          "references" : [ ]
        } ]
      },
      "CaseComment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "CaseComment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "actorType",
          "references" : [ ]
        }, {
          "name" : "createdBy",
          "references" : [ ]
        }, {
          "name" : "createdDate",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "published",
          "references" : [ ]
        }, {
          "name" : "text",
          "references" : [ ]
        } ]
      },
      "Chatter" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subscriptionId",
            "type" : "String"
          } ],
          "name" : "deleteSubscription",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowerPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "recordId",
            "type" : "String"
          } ],
          "name" : "getFollowers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowerPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "recordId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Subscription",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subscriptionId",
            "type" : "String"
          } ],
          "name" : "getSubscription",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ChatterActivity" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterActivity",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "commentCount",
          "references" : [ ]
        }, {
          "name" : "commentReceivedCount",
          "references" : [ ]
        }, {
          "name" : "likeReceivedCount",
          "references" : [ ]
        }, {
          "name" : "postCount",
          "references" : [ ]
        } ]
      },
      "ChatterFavorites" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ConnectApi.FeedFavorite",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "searchText",
            "type" : "String"
          } ],
          "name" : "addFavorite",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedFavorite",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "targetId",
            "type" : "String"
          } ],
          "name" : "addRecordFavorite",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          } ],
          "name" : "deleteFavorite",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedFavorite",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          } ],
          "name" : "getFavorite",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedFavorites",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          } ],
          "name" : "getFavorites",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          } ],
          "name" : "getFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedFavorite",
          "argTypes" : [ "String", "String", "String", "Boolean" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "favoriteId",
            "type" : "String"
          }, {
            "name" : "updateLastViewDate",
            "type" : "Boolean"
          } ],
          "name" : "updateFavorite",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ChatterFeeds" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "commentId",
            "type" : "String"
          } ],
          "name" : "deleteComment",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "deleteFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "likeId",
            "type" : "String"
          } ],
          "name" : "deleteLike",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Comment",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "commentId",
            "type" : "String"
          } ],
          "name" : "getComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.CommentPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "getCommentsForFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.CommentPage",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getCommentsForFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "ConnectApi.FeedType" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          } ],
          "name" : "getFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "ConnectApi.FeedType", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          } ],
          "name" : "getFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItem",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "getFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          } ],
          "name" : "getFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "Integer", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          } ],
          "name" : "getFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String", "Integer", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          } ],
          "name" : "getFeedItemsFromFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFeedItemsFromFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedPoll",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "getFeedPoll",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          } ],
          "name" : "getFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Feed",
          "argTypes" : [ "String", "String", "String", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "getFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLike",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "likeId",
            "type" : "String"
          } ],
          "name" : "getLike",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLikePage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "commentId",
            "type" : "String"
          } ],
          "name" : "getLikesForComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLikePage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "commentId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getLikesForComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLikePage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "getLikesForFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLikePage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getLikesForFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedModifiedInfo",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "since",
            "type" : "String"
          } ],
          "name" : "isModified",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLike",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "commentId",
            "type" : "String"
          } ],
          "name" : "likeComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterLike",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          } ],
          "name" : "likeFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Comment",
          "argTypes" : [ "String", "String", "ConnectApi.CommentInput", "ConnectApi.BinaryInput" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "comment",
            "type" : "ConnectApi.CommentInput"
          }, {
            "name" : "feedItemFileUpload",
            "type" : "ConnectApi.BinaryInput"
          } ],
          "name" : "postComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Comment",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "text",
            "type" : "String"
          } ],
          "name" : "postComment",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItem",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "ConnectApi.FeedItemInput", "ConnectApi.BinaryInput" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "feedItem",
            "type" : "ConnectApi.FeedItemInput"
          }, {
            "name" : "feedItemFileUpload",
            "type" : "ConnectApi.BinaryInput"
          } ],
          "name" : "postFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItem",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "text",
            "type" : "String"
          } ],
          "name" : "postFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "searchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "searchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          } ],
          "name" : "searchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "Integer", "ConnectApi.FeedSortOrder", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItemPage",
          "argTypes" : [ "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchFeedItemsInFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "Integer", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestGetFeedItemsFromFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Integer", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItems",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "Integer", "ConnectApi.FeedSortOrder", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String", "Integer", "ConnectApi.FeedSortOrder", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "String"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "sortParam",
            "type" : "ConnectApi.FeedSortOrder"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String", "ConnectApi.FeedItemPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "keyPrefix",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.FeedItemPage"
          } ],
          "name" : "setTestSearchFeedItemsInFilterFeed",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItem",
          "argTypes" : [ "String", "ConnectApi.FeedType", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedType",
            "type" : "ConnectApi.FeedType"
          }, {
            "name" : "subjectId",
            "type" : "String"
          }, {
            "name" : "originalFeedItemId",
            "type" : "String"
          } ],
          "name" : "shareFeedItem",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedItem",
          "argTypes" : [ "String", "String", "Boolean" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "isBookmarkedByCurrentUser",
            "type" : "Boolean"
          } ],
          "name" : "updateBookmark",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FeedPoll",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "feedItemId",
            "type" : "String"
          }, {
            "name" : "myChoiceId",
            "type" : "String"
          } ],
          "name" : "voteOnFeedPoll",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ChatterGroup" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "canHaveChatterGuests",
          "references" : [ ]
        }, {
          "name" : "community",
          "references" : [ ]
        }, {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "emailToChatterAddress",
          "references" : [ ]
        }, {
          "name" : "lastFeedItemPostDate",
          "references" : [ ]
        }, {
          "name" : "memberCount",
          "references" : [ ]
        }, {
          "name" : "myRole",
          "references" : [ ]
        }, {
          "name" : "owner",
          "references" : [ ]
        }, {
          "name" : "photo",
          "references" : [ ]
        }, {
          "name" : "visibility",
          "references" : [ ]
        } ]
      },
      "ChatterGroupDetail" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterGroupDetail",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "fileCount",
          "references" : [ ]
        }, {
          "name" : "information",
          "references" : [ ]
        } ]
      },
      "ChatterGroupInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterGroupInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "information",
          "references" : [ ]
        } ]
      },
      "ChatterGroupPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterGroupPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "groups",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        } ]
      },
      "ChatterGroupSummary" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterGroupSummary",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "fileCount",
          "references" : [ ]
        } ]
      },
      "ChatterGroups" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ConnectApi.GroupMember",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "addMember",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "membershipId",
            "type" : "String"
          } ],
          "name" : "deleteMember",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "deletePhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Subscription",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          } ],
          "name" : "follow",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupDetail",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getGroup",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMembershipRequest",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "requestId",
            "type" : "String"
          } ],
          "name" : "getGroupMembershipRequest",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMembershipRequests",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getGroupMembershipRequests",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMembershipRequests",
          "argTypes" : [ "String", "String", "ConnectApi.GroupMembershipRequestStatus" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "status",
            "type" : "ConnectApi.GroupMembershipRequestStatus"
          } ],
          "name" : "getGroupMembershipRequests",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupPage",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupPage",
          "argTypes" : [ "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMember",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "membershipId",
            "type" : "String"
          } ],
          "name" : "getMember",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMemberPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getMembers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMemberPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getMembers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupChatterSettings",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getMyChatterSettings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "getPhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMembershipRequest",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          } ],
          "name" : "requestGroupMembership",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "searchGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String", "ConnectApi.BinaryInput" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "fileUpload",
            "type" : "ConnectApi.BinaryInput"
          } ],
          "name" : "setPhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "fileId",
            "type" : "String"
          }, {
            "name" : "versionNumber",
            "type" : "Integer"
          } ],
          "name" : "setPhoto",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "ConnectApi.ChatterGroupPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.ChatterGroupPage"
          } ],
          "name" : "setTestSearchGroups",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "Integer", "Integer", "ConnectApi.ChatterGroupPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "result",
            "type" : "ConnectApi.ChatterGroupPage"
          } ],
          "name" : "setTestSearchGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.ChatterGroupDetail",
          "argTypes" : [ "String", "String", "ConnectApi.ChatterGroupInput" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "groupInput",
            "type" : "ConnectApi.ChatterGroupInput"
          } ],
          "name" : "updateGroup",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupChatterSettings",
          "argTypes" : [ "String", "String", "ConnectApi.GroupEmailFrequency" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "groupId",
            "type" : "String"
          }, {
            "name" : "emailFrequency",
            "type" : "ConnectApi.GroupEmailFrequency"
          } ],
          "name" : "updateMyChatterSettings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.GroupMembershipRequest",
          "argTypes" : [ "String", "String", "ConnectApi.GroupMembershipRequestStatus" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "requestId",
            "type" : "String"
          }, {
            "name" : "status",
            "type" : "ConnectApi.GroupMembershipRequestStatus"
          } ],
          "name" : "updateRequestStatus",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ChatterLike" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterLike",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "likedItem",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "ChatterLikePage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ChatterLikePage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageToken",
          "references" : [ ]
        }, {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "likes",
          "references" : [ ]
        }, {
          "name" : "nextPageToken",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageToken",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "ChatterUsers" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "deletePhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Subscription",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "subjectId",
            "type" : "String"
          } ],
          "name" : "follow",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserChatterSettings",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getChatterSettings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowerPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getFollowers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowerPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.FollowingPage",
          "argTypes" : [ "String", "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "filterType",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getFollowings",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserGroupPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserGroupPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getGroups",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getPhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserDetail",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          } ],
          "name" : "getUser",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserPage",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserPage",
          "argTypes" : [ "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "getUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserPage",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          } ],
          "name" : "searchUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserPage",
          "argTypes" : [ "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "searchUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserPage",
          "argTypes" : [ "String", "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "searchContextId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          } ],
          "name" : "searchUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String", "ConnectApi.BinaryInput" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "fileUpload",
            "type" : "ConnectApi.BinaryInput"
          } ],
          "name" : "setPhoto",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Photo",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "fileId",
            "type" : "String"
          }, {
            "name" : "versionNumber",
            "type" : "Integer"
          } ],
          "name" : "setPhoto",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "ConnectApi.UserPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "result",
            "type" : "ConnectApi.UserPage"
          } ],
          "name" : "setTestSearchUsers",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "Integer", "Integer", "ConnectApi.UserPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "result",
            "type" : "ConnectApi.UserPage"
          } ],
          "name" : "setTestSearchUsers",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Integer", "Integer", "ConnectApi.UserPage" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "q",
            "type" : "String"
          }, {
            "name" : "searchContextId",
            "type" : "String"
          }, {
            "name" : "pageParam",
            "type" : "Integer"
          }, {
            "name" : "pageSize",
            "type" : "Integer"
          }, {
            "name" : "result",
            "type" : "ConnectApi.UserPage"
          } ],
          "name" : "setTestSearchUsers",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.UserChatterSettings",
          "argTypes" : [ "String", "String", "ConnectApi.GroupEmailFrequency" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "defaultGroupEmailFrequency",
            "type" : "ConnectApi.GroupEmailFrequency"
          } ],
          "name" : "updateChatterSettings",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ClientInfo" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ClientInfo",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "applicationName",
          "references" : [ ]
        }, {
          "name" : "applicationUrl",
          "references" : [ ]
        } ]
      },
      "Comment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Comment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "attachment",
          "references" : [ ]
        }, {
          "name" : "body",
          "references" : [ ]
        }, {
          "name" : "clientInfo",
          "references" : [ ]
        }, {
          "name" : "createdDate",
          "references" : [ ]
        }, {
          "name" : "feedItem",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "isDeleteRestricted",
          "references" : [ ]
        }, {
          "name" : "likes",
          "references" : [ ]
        }, {
          "name" : "likesMessage",
          "references" : [ ]
        }, {
          "name" : "myLike",
          "references" : [ ]
        }, {
          "name" : "parent",
          "references" : [ ]
        }, {
          "name" : "relativeCreatedDate",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "CommentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "CommentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "attachment",
          "references" : [ ]
        }, {
          "name" : "body",
          "references" : [ ]
        } ]
      },
      "CommentPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "CommentPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "comments",
          "references" : [ ]
        }, {
          "name" : "currentPageToken",
          "references" : [ ]
        }, {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "nextPageToken",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "CommentType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.CommentType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ContentComment",
          "references" : [ ]
        }, {
          "name" : "TextComment",
          "references" : [ ]
        } ]
      },
      "Communities" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ConnectApi.CommunityPage",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCommunities",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.CommunityPage",
          "argTypes" : [ "ConnectApi.CommunityStatus" ],
          "parameters" : [ {
            "name" : "status",
            "type" : "ConnectApi.CommunityStatus"
          } ],
          "name" : "getCommunities",
          "references" : [ ]
        }, {
          "returnType" : "ConnectApi.Community",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getCommunity",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Community" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Community",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "invitationsEnabled",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "sendWelcomeEmail",
          "references" : [ ]
        }, {
          "name" : "status",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "urlPathPrefix",
          "references" : [ ]
        } ]
      },
      "CommunityPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "CommunityPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "communities",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "CommunityStatus" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.CommunityStatus>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Inactive",
          "references" : [ ]
        }, {
          "name" : "Live",
          "references" : [ ]
        }, {
          "name" : "UnderConstruction",
          "references" : [ ]
        } ]
      },
      "ComplexSegment" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "segments",
          "references" : [ ]
        } ]
      },
      "ConnectApiException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getErrorCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ContentAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ContentAttachment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "checksum",
          "references" : [ ]
        }, {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "downloadUrl",
          "references" : [ ]
        }, {
          "name" : "fileExtension",
          "references" : [ ]
        }, {
          "name" : "fileSize",
          "references" : [ ]
        }, {
          "name" : "fileType",
          "references" : [ ]
        }, {
          "name" : "hasImagePreview",
          "references" : [ ]
        }, {
          "name" : "hasPdfPreview",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "isInMyFileSync",
          "references" : [ ]
        }, {
          "name" : "mimeType",
          "references" : [ ]
        }, {
          "name" : "renditionUrl",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        }, {
          "name" : "versionId",
          "references" : [ ]
        } ]
      },
      "ContentAttachmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ContentAttachmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "contentDocumentId",
          "references" : [ ]
        } ]
      },
      "DashboardComponentAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "DashboardComponentAttachment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "componentId",
          "references" : [ ]
        }, {
          "name" : "componentName",
          "references" : [ ]
        }, {
          "name" : "dashboardBodyText",
          "references" : [ ]
        }, {
          "name" : "dashboardId",
          "references" : [ ]
        }, {
          "name" : "dashboardName",
          "references" : [ ]
        }, {
          "name" : "fullSizeImageUrl",
          "references" : [ ]
        }, {
          "name" : "lastRefreshDate",
          "references" : [ ]
        }, {
          "name" : "lastRefreshDateDisplayText",
          "references" : [ ]
        }, {
          "name" : "runningUser",
          "references" : [ ]
        }, {
          "name" : "thumbnailUrl",
          "references" : [ ]
        } ]
      },
      "EntityLinkSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EntityLinkSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "motif",
          "references" : [ ]
        }, {
          "name" : "reference",
          "references" : [ ]
        } ]
      },
      "Features" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Features",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "chatter",
          "references" : [ ]
        }, {
          "name" : "chatterActivity",
          "references" : [ ]
        }, {
          "name" : "chatterGlobalInfluence",
          "references" : [ ]
        }, {
          "name" : "chatterMessages",
          "references" : [ ]
        }, {
          "name" : "chatterTopics",
          "references" : [ ]
        }, {
          "name" : "dashboardComponentSnapshots",
          "references" : [ ]
        }, {
          "name" : "defaultCurrencyIsoCode",
          "references" : [ ]
        }, {
          "name" : "feedPolling",
          "references" : [ ]
        }, {
          "name" : "files",
          "references" : [ ]
        }, {
          "name" : "filesOnComments",
          "references" : [ ]
        }, {
          "name" : "groupsCanFollow",
          "references" : [ ]
        }, {
          "name" : "multiCurrency",
          "references" : [ ]
        }, {
          "name" : "publisherActions",
          "references" : [ ]
        }, {
          "name" : "thanksAllowed",
          "references" : [ ]
        }, {
          "name" : "trendingTopics",
          "references" : [ ]
        }, {
          "name" : "viralInvitesAllowed",
          "references" : [ ]
        } ]
      },
      "Feed" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Feed",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "feedItemsUrl",
          "references" : [ ]
        }, {
          "name" : "isModifiedUrl",
          "references" : [ ]
        } ]
      },
      "FeedBody" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedBody",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FeedFavorite" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedFavorite",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "community",
          "references" : [ ]
        }, {
          "name" : "createdBy",
          "references" : [ ]
        }, {
          "name" : "feedUrl",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "lastViewDate",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "searchText",
          "references" : [ ]
        }, {
          "name" : "target",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "FeedFavoriteType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedFavoriteType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ListView",
          "references" : [ ]
        }, {
          "name" : "Search",
          "references" : [ ]
        }, {
          "name" : "Topic",
          "references" : [ ]
        } ]
      },
      "FeedFavorites" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedFavorites",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "favorites",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "FeedItem" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedItem",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "actor",
          "references" : [ ]
        }, {
          "name" : "attachment",
          "references" : [ ]
        }, {
          "name" : "body",
          "references" : [ ]
        }, {
          "name" : "canShare",
          "references" : [ ]
        }, {
          "name" : "clientInfo",
          "references" : [ ]
        }, {
          "name" : "comments",
          "references" : [ ]
        }, {
          "name" : "createdDate",
          "references" : [ ]
        }, {
          "name" : "event",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "isBookmarkedByCurrentUser",
          "references" : [ ]
        }, {
          "name" : "isDeleteRestricted",
          "references" : [ ]
        }, {
          "name" : "isLikedByCurrentUser",
          "references" : [ ]
        }, {
          "name" : "likes",
          "references" : [ ]
        }, {
          "name" : "likesMessage",
          "references" : [ ]
        }, {
          "name" : "modifiedDate",
          "references" : [ ]
        }, {
          "name" : "myLike",
          "references" : [ ]
        }, {
          "name" : "originalFeedItem",
          "references" : [ ]
        }, {
          "name" : "originalFeedItemActor",
          "references" : [ ]
        }, {
          "name" : "parent",
          "references" : [ ]
        }, {
          "name" : "photoUrl",
          "references" : [ ]
        }, {
          "name" : "preamble",
          "references" : [ ]
        }, {
          "name" : "relativeCreatedDate",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "visibility",
          "references" : [ ]
        } ]
      },
      "FeedItemAttachment" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "type",
          "references" : [ ]
        } ]
      },
      "FeedItemAttachmentInput" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FeedItemAttachmentType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedItemAttachmentType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Approval",
          "references" : [ ]
        }, {
          "name" : "BasicTemplate",
          "references" : [ ]
        }, {
          "name" : "CaseComment",
          "references" : [ ]
        }, {
          "name" : "Content",
          "references" : [ ]
        }, {
          "name" : "DashboardComponent",
          "references" : [ ]
        }, {
          "name" : "Link",
          "references" : [ ]
        }, {
          "name" : "Poll",
          "references" : [ ]
        } ]
      },
      "FeedItemInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedItemInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "attachment",
          "references" : [ ]
        }, {
          "name" : "body",
          "references" : [ ]
        }, {
          "name" : "isBookmarkedByCurrentUser",
          "references" : [ ]
        }, {
          "name" : "originalFeedItemId",
          "references" : [ ]
        }, {
          "name" : "visibility",
          "references" : [ ]
        } ]
      },
      "FeedItemPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedItemPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageToken",
          "references" : [ ]
        }, {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "isModifiedToken",
          "references" : [ ]
        }, {
          "name" : "isModifiedUrl",
          "references" : [ ]
        }, {
          "name" : "items",
          "references" : [ ]
        }, {
          "name" : "nextPageToken",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        } ]
      },
      "FeedItemType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedItemType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ActivityEvent",
          "references" : [ ]
        }, {
          "name" : "ApprovalPost",
          "references" : [ ]
        }, {
          "name" : "AttachArticleEvent",
          "references" : [ ]
        }, {
          "name" : "BasicTemplateFeedItem",
          "references" : [ ]
        }, {
          "name" : "CallLogPost",
          "references" : [ ]
        }, {
          "name" : "CaseCommentPost",
          "references" : [ ]
        }, {
          "name" : "ChangeStatusPost",
          "references" : [ ]
        }, {
          "name" : "ChatTranscriptPost",
          "references" : [ ]
        }, {
          "name" : "CollaborationGroupCreated",
          "references" : [ ]
        }, {
          "name" : "CollaborationGroupUnarchived",
          "references" : [ ]
        }, {
          "name" : "ContentPost",
          "references" : [ ]
        }, {
          "name" : "CreateRecordEvent",
          "references" : [ ]
        }, {
          "name" : "DashboardComponentAlert",
          "references" : [ ]
        }, {
          "name" : "DashboardComponentSnapshot",
          "references" : [ ]
        }, {
          "name" : "EmailMessageEvent",
          "references" : [ ]
        }, {
          "name" : "FacebookPost",
          "references" : [ ]
        }, {
          "name" : "LinkPost",
          "references" : [ ]
        }, {
          "name" : "PollPost",
          "references" : [ ]
        }, {
          "name" : "ReplyPost",
          "references" : [ ]
        }, {
          "name" : "RypplePost",
          "references" : [ ]
        }, {
          "name" : "TextPost",
          "references" : [ ]
        }, {
          "name" : "TrackedChange",
          "references" : [ ]
        }, {
          "name" : "TwitterPost",
          "references" : [ ]
        }, {
          "name" : "UserStatus",
          "references" : [ ]
        } ]
      },
      "FeedItemVisibilityType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedItemVisibilityType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "AllUsers",
          "references" : [ ]
        }, {
          "name" : "InternalUsers",
          "references" : [ ]
        } ]
      },
      "FeedModifiedInfo" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedModifiedInfo",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "isModified",
          "references" : [ ]
        }, {
          "name" : "isModifiedToken",
          "references" : [ ]
        }, {
          "name" : "nextPollUrl",
          "references" : [ ]
        } ]
      },
      "FeedPoll" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedPoll",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "choices",
          "references" : [ ]
        }, {
          "name" : "myChoiceId",
          "references" : [ ]
        }, {
          "name" : "totalVoteCount",
          "references" : [ ]
        } ]
      },
      "FeedPollChoice" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FeedPollChoice",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "position",
          "references" : [ ]
        }, {
          "name" : "text",
          "references" : [ ]
        }, {
          "name" : "voteCount",
          "references" : [ ]
        }, {
          "name" : "voteCountRatio",
          "references" : [ ]
        } ]
      },
      "FeedSortOrder" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedSortOrder>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "CreatedDateDesc",
          "references" : [ ]
        }, {
          "name" : "LastModifiedDateDesc",
          "references" : [ ]
        } ]
      },
      "FeedType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.FeedType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Bookmarks",
          "references" : [ ]
        }, {
          "name" : "Company",
          "references" : [ ]
        }, {
          "name" : "Files",
          "references" : [ ]
        }, {
          "name" : "Groups",
          "references" : [ ]
        }, {
          "name" : "News",
          "references" : [ ]
        }, {
          "name" : "People",
          "references" : [ ]
        }, {
          "name" : "Record",
          "references" : [ ]
        }, {
          "name" : "To",
          "references" : [ ]
        }, {
          "name" : "Topics",
          "references" : [ ]
        }, {
          "name" : "UserProfile",
          "references" : [ ]
        } ]
      },
      "FieldChangeNameSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FieldChangeNameSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FieldChangeSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FieldChangeSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FieldChangeValueSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FieldChangeValueSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "FileSummary" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FileSummary",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "checksum",
          "references" : [ ]
        }, {
          "name" : "contentSize",
          "references" : [ ]
        }, {
          "name" : "contentUrl",
          "references" : [ ]
        }, {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "downloadUrl",
          "references" : [ ]
        }, {
          "name" : "fileExtension",
          "references" : [ ]
        }, {
          "name" : "fileType",
          "references" : [ ]
        }, {
          "name" : "flashRenditionStatus",
          "references" : [ ]
        }, {
          "name" : "isInMyFileSync",
          "references" : [ ]
        }, {
          "name" : "mimeType",
          "references" : [ ]
        }, {
          "name" : "modifiedDate",
          "references" : [ ]
        }, {
          "name" : "origin",
          "references" : [ ]
        }, {
          "name" : "owner",
          "references" : [ ]
        }, {
          "name" : "pdfRenditionStatus",
          "references" : [ ]
        }, {
          "name" : "renditionUrl",
          "references" : [ ]
        }, {
          "name" : "thumb120By90RenditionStatus",
          "references" : [ ]
        }, {
          "name" : "thumb240By180RenditionStatus",
          "references" : [ ]
        }, {
          "name" : "thumb720By480RenditionStatus",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        }, {
          "name" : "versionNumber",
          "references" : [ ]
        } ]
      },
      "FollowerPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FollowerPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "followers",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "FollowingCounts" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FollowingCounts",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "people",
          "references" : [ ]
        }, {
          "name" : "records",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "FollowingPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "FollowingPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "following",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "GlobalInfluence" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GlobalInfluence",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "percentile",
          "references" : [ ]
        }, {
          "name" : "rank",
          "references" : [ ]
        } ]
      },
      "GroupChatterSettings" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupChatterSettings",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "emailFrequency",
          "references" : [ ]
        } ]
      },
      "GroupEmailFrequency" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.GroupEmailFrequency>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "DailyDigest",
          "references" : [ ]
        }, {
          "name" : "EachPost",
          "references" : [ ]
        }, {
          "name" : "Never",
          "references" : [ ]
        }, {
          "name" : "UseDefault",
          "references" : [ ]
        }, {
          "name" : "WeeklyDigest",
          "references" : [ ]
        } ]
      },
      "GroupInformation" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupInformation",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "text",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        } ]
      },
      "GroupInformationInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupInformationInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "text",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        } ]
      },
      "GroupMember" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupMember",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "role",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "GroupMemberPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupMemberPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "members",
          "references" : [ ]
        }, {
          "name" : "myMembership",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "totalMemberCount",
          "references" : [ ]
        } ]
      },
      "GroupMembershipRequest" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupMembershipRequest",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "createdDate",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "lastUpdateDate",
          "references" : [ ]
        }, {
          "name" : "requestedGroup",
          "references" : [ ]
        }, {
          "name" : "responseMessage",
          "references" : [ ]
        }, {
          "name" : "status",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "GroupMembershipRequestStatus" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.GroupMembershipRequestStatus>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Accepted",
          "references" : [ ]
        }, {
          "name" : "Declined",
          "references" : [ ]
        }, {
          "name" : "Pending",
          "references" : [ ]
        } ]
      },
      "GroupMembershipRequests" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "GroupMembershipRequests",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "requests",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "GroupMembershipType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.GroupMembershipType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "GroupManager",
          "references" : [ ]
        }, {
          "name" : "GroupOwner",
          "references" : [ ]
        }, {
          "name" : "NotAMember",
          "references" : [ ]
        }, {
          "name" : "NotAMemberPrivateRequested",
          "references" : [ ]
        }, {
          "name" : "StandardMember",
          "references" : [ ]
        } ]
      },
      "GroupVisibilityType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.GroupVisibilityType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "PrivateAccess",
          "references" : [ ]
        }, {
          "name" : "PublicAccess",
          "references" : [ ]
        } ]
      },
      "HashtagSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "HashtagSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "tag",
          "references" : [ ]
        }, {
          "name" : "topicUrl",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "HashtagSegmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "HashtagSegmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "tag",
          "references" : [ ]
        } ]
      },
      "Icon" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Icon",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "height",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "width",
          "references" : [ ]
        } ]
      },
      "LinkAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "LinkAttachment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "title",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "LinkAttachmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "LinkAttachmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "url",
          "references" : [ ]
        }, {
          "name" : "urlName",
          "references" : [ ]
        } ]
      },
      "LinkSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "LinkSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "LinkSegmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "LinkSegmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "MentionSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MentionSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "accessible",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "user",
          "references" : [ ]
        } ]
      },
      "MentionSegmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MentionSegmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        } ]
      },
      "MessageBody" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MessageBody",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "MessageBodyInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MessageBodyInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "messageSegments",
          "references" : [ ]
        } ]
      },
      "MessageSegment" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "text",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        } ]
      },
      "MessageSegmentInput" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "MessageSegmentType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.MessageSegmentType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "EntityLink",
          "references" : [ ]
        }, {
          "name" : "FieldChange",
          "references" : [ ]
        }, {
          "name" : "FieldChangeName",
          "references" : [ ]
        }, {
          "name" : "FieldChangeValue",
          "references" : [ ]
        }, {
          "name" : "Hashtag",
          "references" : [ ]
        }, {
          "name" : "Link",
          "references" : [ ]
        }, {
          "name" : "Mention",
          "references" : [ ]
        }, {
          "name" : "MoreChanges",
          "references" : [ ]
        }, {
          "name" : "ResourceLink",
          "references" : [ ]
        }, {
          "name" : "Text",
          "references" : [ ]
        } ]
      },
      "MoreChangesSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MoreChangesSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "moreChangesCount",
          "references" : [ ]
        } ]
      },
      "Motif" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Motif",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "largeIconUrl",
          "references" : [ ]
        }, {
          "name" : "mediumIconUrl",
          "references" : [ ]
        }, {
          "name" : "smallIconUrl",
          "references" : [ ]
        } ]
      },
      "NewFileAttachmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "NewFileAttachmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        } ]
      },
      "NotFoundException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Organization" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ConnectApi.OrganizationSettings",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSettings",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "OrganizationSettings" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "OrganizationSettings",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "accessTimeout",
          "references" : [ ]
        }, {
          "name" : "features",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "orgId",
          "references" : [ ]
        }, {
          "name" : "userSettings",
          "references" : [ ]
        } ]
      },
      "PhoneNumber" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "PhoneNumber",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "phoneNumber",
          "references" : [ ]
        }, {
          "name" : "type",
          "references" : [ ]
        } ]
      },
      "Photo" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Photo",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "fullEmailPhotoUrl",
          "references" : [ ]
        }, {
          "name" : "largePhotoUrl",
          "references" : [ ]
        }, {
          "name" : "photoVersionId",
          "references" : [ ]
        }, {
          "name" : "smallPhotoUrl",
          "references" : [ ]
        }, {
          "name" : "standardEmailPhotoUrl",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "PollAttachmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "PollAttachmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "pollChoices",
          "references" : [ ]
        } ]
      },
      "RateLimitException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getErrorCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "RecordSummary" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "RecordSummary",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Records" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "ConnectApi.Motif",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "communityId",
            "type" : "String"
          }, {
            "name" : "idOrPrefix",
            "type" : "String"
          } ],
          "name" : "getMotif",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Reference" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Reference",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "ResourceLinkSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "ResourceLinkSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "Subscription" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Subscription",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "community",
          "references" : [ ]
        }, {
          "name" : "id",
          "references" : [ ]
        }, {
          "name" : "subject",
          "references" : [ ]
        }, {
          "name" : "subscriber",
          "references" : [ ]
        }, {
          "name" : "url",
          "references" : [ ]
        } ]
      },
      "TextSegment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "TextSegment",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "TextSegmentInput" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "TextSegmentInput",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "java:java.lang.Object",
          "argTypes" : [ "java:common.api.AppVersion" ],
          "parameters" : [ {
            "name" : "currentVersion",
            "type" : "java:common.api.AppVersion"
          } ],
          "name" : "convertToJavaObject",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "text",
          "references" : [ ]
        } ]
      },
      "UnauthenticatedUser" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UnauthenticatedUser",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "User" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "companyName",
          "references" : [ ]
        }, {
          "name" : "firstName",
          "references" : [ ]
        }, {
          "name" : "isInThisCommunity",
          "references" : [ ]
        }, {
          "name" : "lastName",
          "references" : [ ]
        }, {
          "name" : "photo",
          "references" : [ ]
        }, {
          "name" : "title",
          "references" : [ ]
        }, {
          "name" : "userType",
          "references" : [ ]
        } ]
      },
      "UserChatterSettings" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserChatterSettings",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "defaultGroupEmailFrequency",
          "references" : [ ]
        } ]
      },
      "UserDetail" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserDetail",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "aboutMe",
          "references" : [ ]
        }, {
          "name" : "address",
          "references" : [ ]
        }, {
          "name" : "chatterActivity",
          "references" : [ ]
        }, {
          "name" : "chatterInfluence",
          "references" : [ ]
        }, {
          "name" : "email",
          "references" : [ ]
        }, {
          "name" : "followersCount",
          "references" : [ ]
        }, {
          "name" : "followingCounts",
          "references" : [ ]
        }, {
          "name" : "groupCount",
          "references" : [ ]
        }, {
          "name" : "isActive",
          "references" : [ ]
        }, {
          "name" : "managerId",
          "references" : [ ]
        }, {
          "name" : "managerName",
          "references" : [ ]
        }, {
          "name" : "phoneNumbers",
          "references" : [ ]
        }, {
          "name" : "username",
          "references" : [ ]
        } ]
      },
      "UserGroupPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserGroupPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "groups",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "total",
          "references" : [ ]
        } ]
      },
      "UserPage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserPage",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "currentPageToken",
          "references" : [ ]
        }, {
          "name" : "currentPageUrl",
          "references" : [ ]
        }, {
          "name" : "nextPageToken",
          "references" : [ ]
        }, {
          "name" : "nextPageUrl",
          "references" : [ ]
        }, {
          "name" : "previousPageToken",
          "references" : [ ]
        }, {
          "name" : "previousPageUrl",
          "references" : [ ]
        }, {
          "name" : "users",
          "references" : [ ]
        } ]
      },
      "UserSettings" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserSettings",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBuildVersion",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "approvalPosts",
          "references" : [ ]
        }, {
          "name" : "canFollow",
          "references" : [ ]
        }, {
          "name" : "canModifyAllData",
          "references" : [ ]
        }, {
          "name" : "canOwnGroups",
          "references" : [ ]
        }, {
          "name" : "canViewAllData",
          "references" : [ ]
        }, {
          "name" : "canViewAllGroups",
          "references" : [ ]
        }, {
          "name" : "canViewAllUsers",
          "references" : [ ]
        }, {
          "name" : "canViewFullUserProfile",
          "references" : [ ]
        }, {
          "name" : "canViewPublicFiles",
          "references" : [ ]
        }, {
          "name" : "currencySymbol",
          "references" : [ ]
        }, {
          "name" : "externalUser",
          "references" : [ ]
        }, {
          "name" : "hasAccessToInternalOrg",
          "references" : [ ]
        }, {
          "name" : "hasFileSync",
          "references" : [ ]
        }, {
          "name" : "userDefaultCurrencyIsoCode",
          "references" : [ ]
        }, {
          "name" : "userId",
          "references" : [ ]
        }, {
          "name" : "userLocale",
          "references" : [ ]
        } ]
      },
      "UserSummary" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserSummary",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "obj",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "isActive",
          "references" : [ ]
        } ]
      },
      "UserType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.UserType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ChatterGuest",
          "references" : [ ]
        }, {
          "name" : "ChatterOnly",
          "references" : [ ]
        }, {
          "name" : "Guest",
          "references" : [ ]
        }, {
          "name" : "Internal",
          "references" : [ ]
        }, {
          "name" : "Portal",
          "references" : [ ]
        }, {
          "name" : "System",
          "references" : [ ]
        }, {
          "name" : "Undefined",
          "references" : [ ]
        } ]
      },
      "WorkflowProcessStatus" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<ConnectApi.WorkflowProcessStatus>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "Approved",
          "references" : [ ]
        }, {
          "name" : "Fault",
          "references" : [ ]
        }, {
          "name" : "Held",
          "references" : [ ]
        }, {
          "name" : "NoResponse",
          "references" : [ ]
        }, {
          "name" : "Pending",
          "references" : [ ]
        }, {
          "name" : "Reassigned",
          "references" : [ ]
        }, {
          "name" : "Rejected",
          "references" : [ ]
        }, {
          "name" : "Removed",
          "references" : [ ]
        }, {
          "name" : "Started",
          "references" : [ ]
        } ]
      }
    },
    "Database" : {
      "AssignmentRuleHeader" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "AssignmentRuleHeader",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "AssignmentRuleId",
          "references" : [ ]
        }, {
          "name" : "UseDefaultRule",
          "references" : [ ]
        } ]
      },
      "Batchable" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "Database.BatchableContext", "LIST<ANY>" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Database.BatchableContext"
          }, {
            "name" : "param2",
            "type" : "LIST<ANY>"
          } ],
          "name" : "execute",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Database.BatchableContext" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Database.BatchableContext"
          } ],
          "name" : "finish",
          "references" : [ ]
        }, {
          "returnType" : "system.Iterable",
          "argTypes" : [ "Database.BatchableContext" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Database.BatchableContext"
          } ],
          "name" : "start",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "BatchableContext" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getChildJobId",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getJobId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "BatchableContextImpl" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getChildJobId",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getJobId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "DMLOptions" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "DMLOptions",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "AllowFieldTruncation",
          "references" : [ ]
        }, {
          "name" : "AssignmentRuleHeader",
          "references" : [ ]
        }, {
          "name" : "EmailHeader",
          "references" : [ ]
        }, {
          "name" : "LocaleOptions",
          "references" : [ ]
        }, {
          "name" : "OptAllOrNone",
          "references" : [ ]
        } ]
      },
      "EmailHeader" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EmailHeader",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "TriggerAutoResponseEmail",
          "references" : [ ]
        }, {
          "name" : "TriggerOtherEmail",
          "references" : [ ]
        }, {
          "name" : "TriggerUserEmail",
          "references" : [ ]
        } ]
      },
      "LeadConvert" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "QueryLocator" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getQuery",
          "references" : [ ]
        }, {
          "returnType" : "Database.QueryLocatorIterator",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "iterator",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "QueryLocatorChunkIterator" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasNext",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "QueryLocatorIterator" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasNext",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "Flow" : {
      "Interview" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Object",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          } ],
          "name" : "getVariableValue",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "KbManagement" : {
      "PublishingService" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "PublishingService",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "Datetime" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "scheduledDate",
            "type" : "Datetime"
          } ],
          "name" : "archiveOnlineArticle",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Datetime", "Boolean" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "assigneeId",
            "type" : "String"
          }, {
            "name" : "instructions",
            "type" : "String"
          }, {
            "name" : "dueDate",
            "type" : "Datetime"
          }, {
            "name" : "sendEmailNotification",
            "type" : "Boolean"
          } ],
          "name" : "assignDraftArticleTask",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Datetime", "Boolean" ],
          "parameters" : [ {
            "name" : "translationVersionId",
            "type" : "String"
          }, {
            "name" : "assigneeId",
            "type" : "String"
          }, {
            "name" : "instructions",
            "type" : "String"
          }, {
            "name" : "dueDate",
            "type" : "Datetime"
          }, {
            "name" : "sendEmailNotification",
            "type" : "Boolean"
          } ],
          "name" : "assignDraftTranslationTask",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          } ],
          "name" : "cancelScheduledArchivingOfArticle",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          } ],
          "name" : "cancelScheduledPublicationOfArticle",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleVersionId",
            "type" : "String"
          } ],
          "name" : "completeTranslation",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          } ],
          "name" : "deleteArchivedArticle",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "versionNumber",
            "type" : "Integer"
          } ],
          "name" : "deleteArchivedArticleVersion",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          } ],
          "name" : "deleteDraftArticle",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleVersionId",
            "type" : "String"
          } ],
          "name" : "deleteDraftTranslation",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          } ],
          "name" : "editArchivedArticle",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "unpublish",
            "type" : "Boolean"
          } ],
          "name" : "editOnlineArticle",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "Boolean" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "language",
            "type" : "String"
          }, {
            "name" : "unpublish",
            "type" : "Boolean"
          } ],
          "name" : "editPublishedTranslation",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "flagAsNew",
            "type" : "Boolean"
          } ],
          "name" : "publishArticle",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "versionNumber",
            "type" : "Integer"
          } ],
          "name" : "restoreOldVersion",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Datetime" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "scheduledDate",
            "type" : "Datetime"
          } ],
          "name" : "scheduleForPublication",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "articleVersionId",
            "type" : "String"
          } ],
          "name" : "setTranslationToIncomplete",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "String", "Datetime" ],
          "parameters" : [ {
            "name" : "articleId",
            "type" : "String"
          }, {
            "name" : "language",
            "type" : "String"
          }, {
            "name" : "assigneeId",
            "type" : "String"
          }, {
            "name" : "dueDate",
            "type" : "Datetime"
          } ],
          "name" : "submitForTranslation",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "Messaging" : {
      "BinaryAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "BinaryAttachment",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "body",
          "references" : [ ]
        }, {
          "name" : "fileName",
          "references" : [ ]
        }, {
          "name" : "mimeTypeSubType",
          "references" : [ ]
        } ]
      },
      "EmailAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "EmailFileAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "EmailToSalesforceHandler" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EmailToSalesforceHandler",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "Header" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Header",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "value",
          "references" : [ ]
        } ]
      },
      "InboundEmail" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "InboundEmail",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "binaryAttachments",
          "references" : [ ]
        }, {
          "name" : "ccAddresses",
          "references" : [ ]
        }, {
          "name" : "fromAddress",
          "references" : [ ]
        }, {
          "name" : "fromName",
          "references" : [ ]
        }, {
          "name" : "headers",
          "references" : [ ]
        }, {
          "name" : "htmlBody",
          "references" : [ ]
        }, {
          "name" : "htmlBodyIsTruncated",
          "references" : [ ]
        }, {
          "name" : "inReplyTo",
          "references" : [ ]
        }, {
          "name" : "messageId",
          "references" : [ ]
        }, {
          "name" : "plainTextBody",
          "references" : [ ]
        }, {
          "name" : "plainTextBodyIsTruncated",
          "references" : [ ]
        }, {
          "name" : "references",
          "references" : [ ]
        }, {
          "name" : "replyTo",
          "references" : [ ]
        }, {
          "name" : "subject",
          "references" : [ ]
        }, {
          "name" : "textAttachments",
          "references" : [ ]
        }, {
          "name" : "toAddresses",
          "references" : [ ]
        } ]
      },
      "InboundEmailHandler" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Messaging.InboundEmailResult",
          "argTypes" : [ "Messaging.InboundEmail", "Messaging.InboundEnvelope" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Messaging.InboundEmail"
          }, {
            "name" : "param2",
            "type" : "Messaging.InboundEnvelope"
          } ],
          "name" : "handleInboundEmail",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "InboundEmailResult" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "InboundEmailResult",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "message",
          "references" : [ ]
        }, {
          "name" : "success",
          "references" : [ ]
        } ]
      },
      "InboundEnvelope" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "InboundEnvelope",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "fromAddress",
          "references" : [ ]
        }, {
          "name" : "toAddress",
          "references" : [ ]
        } ]
      },
      "MassEmailMessage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "SingleEmailMessage" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "TextAttachment" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "TextAttachment",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "body",
          "references" : [ ]
        }, {
          "name" : "bodyIsTruncated",
          "references" : [ ]
        }, {
          "name" : "charset",
          "references" : [ ]
        }, {
          "name" : "fileName",
          "references" : [ ]
        }, {
          "name" : "mimeTypeSubType",
          "references" : [ ]
        } ]
      }
    },
    "MobilePNS" : {
      "MobilePushNotification" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MobilePushNotification",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "payload",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "MobilePushNotification",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "SET<String>" ],
          "parameters" : [ {
            "name" : "application",
            "type" : "String"
          }, {
            "name" : "users",
            "type" : "SET<String>"
          } ],
          "name" : "send",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "MAP<String,ANY>" ],
          "parameters" : [ {
            "name" : "payload",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "setPayload",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "ttl",
            "type" : "Integer"
          } ],
          "name" : "setTtl",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "MobilePushPayload" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MobilePushPayload",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "MAP<String,ANY>",
          "argTypes" : [ "String", "String", "Integer", "MAP<String,ANY>" ],
          "parameters" : [ {
            "name" : "alert",
            "type" : "String"
          }, {
            "name" : "sound",
            "type" : "String"
          }, {
            "name" : "badgeCount",
            "type" : "Integer"
          }, {
            "name" : "userData",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "apple",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,ANY>",
          "argTypes" : [ "String", "String", "String", "LIST<String>", "String", "String", "Integer", "MAP<String,ANY>" ],
          "parameters" : [ {
            "name" : "alertBody",
            "type" : "String"
          }, {
            "name" : "actionLocKey",
            "type" : "String"
          }, {
            "name" : "locKey",
            "type" : "String"
          }, {
            "name" : "locArgs",
            "type" : "LIST<String>"
          }, {
            "name" : "launchImage",
            "type" : "String"
          }, {
            "name" : "sound",
            "type" : "String"
          }, {
            "name" : "badgeCount",
            "type" : "Integer"
          }, {
            "name" : "userData",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "apple",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "Process" : {
      "InputParameter" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "parameterType",
            "type" : "Process.PluginDescribeResult.ParameterType"
          }, {
            "name" : "required",
            "type" : "Boolean"
          } ],
          "name" : "InputParameter",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "description",
            "type" : "String"
          }, {
            "name" : "parameterType",
            "type" : "Process.PluginDescribeResult.ParameterType"
          }, {
            "name" : "required",
            "type" : "Boolean"
          } ],
          "name" : "InputParameter",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "parameterType",
          "references" : [ ]
        }, {
          "name" : "required",
          "references" : [ ]
        } ]
      },
      "OutputParameter" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "parameterType",
            "type" : "Process.PluginDescribeResult.ParameterType"
          } ],
          "name" : "OutputParameter",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "description",
            "type" : "String"
          }, {
            "name" : "parameterType",
            "type" : "Process.PluginDescribeResult.ParameterType"
          } ],
          "name" : "OutputParameter",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "parameterType",
          "references" : [ ]
        } ]
      },
      "ParameterType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<Process.PluginDescribeResult.ParameterType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "BOOLEAN",
          "references" : [ ]
        }, {
          "name" : "DATE",
          "references" : [ ]
        }, {
          "name" : "DATETIME",
          "references" : [ ]
        }, {
          "name" : "DECIMAL",
          "references" : [ ]
        }, {
          "name" : "DOUBLE",
          "references" : [ ]
        }, {
          "name" : "FLOAT",
          "references" : [ ]
        }, {
          "name" : "ID",
          "references" : [ ]
        }, {
          "name" : "INTEGER",
          "references" : [ ]
        }, {
          "name" : "LONG",
          "references" : [ ]
        }, {
          "name" : "STRING",
          "references" : [ ]
        } ]
      },
      "Plugin" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Process.PluginDescribeResult",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "describe",
          "references" : [ ]
        }, {
          "returnType" : "Process.PluginResult",
          "argTypes" : [ "Process.PluginRequest" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Process.PluginRequest"
          } ],
          "name" : "invoke",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "PluginDescribeResult" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "PluginDescribeResult",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "description",
          "references" : [ ]
        }, {
          "name" : "inputParameters",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "outputParameters",
          "references" : [ ]
        }, {
          "name" : "tag",
          "references" : [ ]
        } ]
      },
      "PluginRequest" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "inputParameters",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "PluginRequest",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "inputParameters",
          "references" : [ ]
        } ]
      },
      "PluginResult" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "outputParameters",
            "type" : "MAP<String,ANY>"
          } ],
          "name" : "PluginResult",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "outputKey",
            "type" : "String"
          }, {
            "name" : "outputValue",
            "type" : "Object"
          } ],
          "name" : "PluginResult",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "outputParameters",
          "references" : [ ]
        } ]
      },
      "SparkPlugApi" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "SparkPlugApi",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Process.SparkPlugApi.SparkPlugDescribeResult",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "className",
            "type" : "String"
          } ],
          "name" : "describePlugin",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Process.SparkPlugApi.SparkPlugDescribeResult>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "describePlugins",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "className",
            "type" : "String"
          }, {
            "name" : "parameters",
            "type" : "String"
          } ],
          "name" : "invokePluginWithJson",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SparkPlugDescribeResult" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "SparkPlugDescribeResult",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "inputParameters",
          "references" : [ ]
        }, {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "outputParameters",
          "references" : [ ]
        } ]
      },
      "SparkPlugParameter" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "SparkPlugParameter",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "name",
          "references" : [ ]
        }, {
          "name" : "parameterType",
          "references" : [ ]
        }, {
          "name" : "required",
          "references" : [ ]
        } ]
      }
    },
    "Schema" : {
      "DataCategoryGroupSobjectTypePair" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      },
      "DisplayType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<Schema.DisplayType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ANYTYPE",
          "references" : [ ]
        }, {
          "name" : "BASE64",
          "references" : [ ]
        }, {
          "name" : "BOOLEAN",
          "references" : [ ]
        }, {
          "name" : "COMBOBOX",
          "references" : [ ]
        }, {
          "name" : "COMPLEXVALUE",
          "references" : [ ]
        }, {
          "name" : "CURRENCY",
          "references" : [ ]
        }, {
          "name" : "DATACATEGORYGROUPREFERENCE",
          "references" : [ ]
        }, {
          "name" : "DATE",
          "references" : [ ]
        }, {
          "name" : "DATETIME",
          "references" : [ ]
        }, {
          "name" : "DOUBLE",
          "references" : [ ]
        }, {
          "name" : "EMAIL",
          "references" : [ ]
        }, {
          "name" : "ENCRYPTEDSTRING",
          "references" : [ ]
        }, {
          "name" : "ID",
          "references" : [ ]
        }, {
          "name" : "INTEGER",
          "references" : [ ]
        }, {
          "name" : "LOCATION",
          "references" : [ ]
        }, {
          "name" : "MULTIPICKLIST",
          "references" : [ ]
        }, {
          "name" : "PERCENT",
          "references" : [ ]
        }, {
          "name" : "PHONE",
          "references" : [ ]
        }, {
          "name" : "PICKLIST",
          "references" : [ ]
        }, {
          "name" : "REFERENCE",
          "references" : [ ]
        }, {
          "name" : "STRING",
          "references" : [ ]
        }, {
          "name" : "TEXTAREA",
          "references" : [ ]
        }, {
          "name" : "TIME",
          "references" : [ ]
        }, {
          "name" : "URL",
          "references" : [ ]
        } ]
      },
      "SObjectField" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Schema.DescribeFieldResult",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDescribe",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SObjectType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Schema.DescribeSObjectResult",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDescribe",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "newSObject",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Id" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          } ],
          "name" : "newSObject",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Id", "Boolean" ],
          "parameters" : [ {
            "name" : "recordTypeId",
            "type" : "Id"
          }, {
            "name" : "loadDefaultValues",
            "type" : "Boolean"
          } ],
          "name" : "newSObject",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SoapType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<Schema.SoapType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ANYTYPE",
          "references" : [ ]
        }, {
          "name" : "BASE64BINARY",
          "references" : [ ]
        }, {
          "name" : "BOOLEAN",
          "references" : [ ]
        }, {
          "name" : "DATE",
          "references" : [ ]
        }, {
          "name" : "DATETIME",
          "references" : [ ]
        }, {
          "name" : "DOUBLE",
          "references" : [ ]
        }, {
          "name" : "EXECUTIONOVERLAY_APEXRESULT",
          "references" : [ ]
        }, {
          "name" : "EXECUTIONOVERLAY_HEAPDUMP",
          "references" : [ ]
        }, {
          "name" : "EXECUTIONOVERLAY_SOQLRESULT",
          "references" : [ ]
        }, {
          "name" : "ID",
          "references" : [ ]
        }, {
          "name" : "INTEGER",
          "references" : [ ]
        }, {
          "name" : "METADATA_APEXCLASS",
          "references" : [ ]
        }, {
          "name" : "METADATA_APEXCOMPONENT",
          "references" : [ ]
        }, {
          "name" : "METADATA_APEXPAGE",
          "references" : [ ]
        }, {
          "name" : "METADATA_APEXTRIGGER",
          "references" : [ ]
        }, {
          "name" : "METADATA_CUSTOMFIELD",
          "references" : [ ]
        }, {
          "name" : "METADATA_CUSTOMOBJECT",
          "references" : [ ]
        }, {
          "name" : "STRING",
          "references" : [ ]
        }, {
          "name" : "SYMBOLTABLE",
          "references" : [ ]
        }, {
          "name" : "TIME",
          "references" : [ ]
        } ]
      }
    },
    "Site" : {
      "UrlRewriter" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<System.PageReference>",
          "argTypes" : [ "LIST<System.PageReference>" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "LIST<System.PageReference>"
          } ],
          "name" : "generateUrlFor",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "System.PageReference" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "System.PageReference"
          } ],
          "name" : "mapRequestUrl",
          "references" : [ ]
        } ],
        "properties" : [ ]
      }
    },
    "Support" : {
      "EmailTemplateSelector" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Id",
          "argTypes" : [ "Id" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Id"
          } ],
          "name" : "getDefaultEmailTemplateId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "EmailToCaseHandler" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EmailToCaseHandler",
          "references" : [ ]
        } ],
        "methods" : [ ],
        "properties" : [ ]
      }
    },
    "System" : {
      "Answers" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Answers",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "question",
            "type" : "SObject"
          } ],
          "name" : "findSimilar",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "questionId",
            "type" : "String"
          }, {
            "name" : "bestReplyId",
            "type" : "String"
          } ],
          "name" : "setBestReply",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ApexPages" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "ApexPages.Message" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "ApexPages.Message"
          } ],
          "name" : "addMessage",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "ex",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addMessages",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "currentPage",
          "references" : [ ]
        }, {
          "returnType" : "LIST<ApexPages.Message>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessages",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasMessages",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "ApexPages.Severity" ],
          "parameters" : [ {
            "name" : "severity",
            "type" : "ApexPages.Severity"
          } ],
          "name" : "hasMessages",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "AppExchange" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "AppExchange",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "testUserName",
            "type" : "String"
          }, {
            "name" : "testCronString",
            "type" : "String"
          } ],
          "name" : "calculateListingPopularity",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "String", "String", "String", "String", "String", "String", "Boolean" ],
          "parameters" : [ {
            "name" : "firstName",
            "type" : "String"
          }, {
            "name" : "lastName",
            "type" : "String"
          }, {
            "name" : "companyName",
            "type" : "String"
          }, {
            "name" : "email",
            "type" : "String"
          }, {
            "name" : "language",
            "type" : "String"
          }, {
            "name" : "adminUserName",
            "type" : "String"
          }, {
            "name" : "packageId",
            "type" : "String"
          }, {
            "name" : "evalUserName",
            "type" : "String"
          }, {
            "name" : "isExtension",
            "type" : "Boolean"
          } ],
          "name" : "createOrg",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "accountId",
            "type" : "String"
          } ],
          "name" : "createPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "appExchangeOrgId",
            "type" : "String"
          }, {
            "name" : "portalId",
            "type" : "String"
          }, {
            "name" : "siteId",
            "type" : "String"
          }, {
            "name" : "portalUserId",
            "type" : "String"
          } ],
          "name" : "createSession",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "debug",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "page",
            "type" : "String"
          } ],
          "name" : "getAuthenticatingUrl",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "section",
            "type" : "String"
          }, {
            "name" : "key",
            "type" : "String"
          } ],
          "name" : "getConfig",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          } ],
          "name" : "getCookie",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Double", "String" ],
          "parameters" : [ {
            "name" : "appVersion",
            "type" : "Double"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "getCrossInstanceEncryptedHash",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "orgId",
            "type" : "String"
          } ],
          "name" : "getInstalledPackageVersions",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "orgId",
            "type" : "String"
          } ],
          "name" : "getOrgName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "pkgVersionId",
            "type" : "String"
          } ],
          "name" : "getPackageManifest",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPortalAdminId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPortalId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSiteId",
          "references" : [ ]
        }, {
          "returnType" : "LIST<TrialTemplate>",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "callerOrgId",
            "type" : "String"
          }, {
            "name" : "lmPkgId",
            "type" : "String"
          }, {
            "name" : "username",
            "type" : "String"
          } ],
          "name" : "getTrialTemplates",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          } ],
          "name" : "isDuplicateUserName",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isGuestUser",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "location",
            "type" : "String"
          } ],
          "name" : "movedPermanently",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "Integer", "Date", "String" ],
          "parameters" : [ {
            "name" : "orgId",
            "type" : "String"
          }, {
            "name" : "allPackageId",
            "type" : "String"
          }, {
            "name" : "numLicenses",
            "type" : "Integer"
          }, {
            "name" : "expirationDate",
            "type" : "Date"
          }, {
            "name" : "status",
            "type" : "String"
          } ],
          "name" : "provisionPackageLicense",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "pkgVersionId",
            "type" : "String"
          } ],
          "name" : "registerPackageVersion",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "setCookie",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Integer" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          }, {
            "name" : "cookieDomainName",
            "type" : "String"
          }, {
            "name" : "cookieAge",
            "type" : "Integer"
          } ],
          "name" : "setCookie",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "pkgVersionId",
            "type" : "String"
          }, {
            "name" : "orgId",
            "type" : "String"
          }, {
            "name" : "defaultLicenseStatus",
            "type" : "String"
          }, {
            "name" : "defaultLicenseLength",
            "type" : "Integer"
          }, {
            "name" : "defaultLicenseSeats",
            "type" : "Integer"
          } ],
          "name" : "setDefaultLicenseTerms",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "statusCode",
            "type" : "Integer"
          } ],
          "name" : "setHttpResponseStatus",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "pkgVersionId",
            "type" : "String"
          }, {
            "name" : "orgId",
            "type" : "String"
          }, {
            "name" : "username",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "setLicenseManagementOrganization",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "stopListingPopularityJob",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "String"
          } ],
          "name" : "to15",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "String"
          } ],
          "name" : "to18",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobj",
            "type" : "SObject"
          } ],
          "name" : "updateSingleAsAdmin",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "validateLMAInstalled",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "validateOrgUser",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ApplicationReadWriteMode" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.ApplicationReadWriteMode>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "DEFAULT",
          "references" : [ ]
        }, {
          "name" : "READ_ONLY",
          "references" : [ ]
        } ]
      },
      "AssertException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "AsyncException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Blob" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "size",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "String"
          } ],
          "name" : "toPdf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Boolean" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "a",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "BusinessHours" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "BusinessHours",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Datetime",
          "argTypes" : [ "Id", "Datetime", "Long" ],
          "parameters" : [ {
            "name" : "businessHoursId",
            "type" : "Id"
          }, {
            "name" : "startDate",
            "type" : "Datetime"
          }, {
            "name" : "interval",
            "type" : "Long"
          } ],
          "name" : "add",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Id", "Datetime", "Long" ],
          "parameters" : [ {
            "name" : "businessHoursId",
            "type" : "Id"
          }, {
            "name" : "startDate",
            "type" : "Datetime"
          }, {
            "name" : "interval",
            "type" : "Long"
          } ],
          "name" : "addGmt",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "String", "Datetime", "Datetime" ],
          "parameters" : [ {
            "name" : "businessHoursId",
            "type" : "String"
          }, {
            "name" : "startDate",
            "type" : "Datetime"
          }, {
            "name" : "endDate",
            "type" : "Datetime"
          } ],
          "name" : "diff",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "CURRENCY" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "formatAmount",
          "references" : [ ]
        }, {
          "returnType" : "CURRENCY",
          "argTypes" : [ "Decimal", "String" ],
          "parameters" : [ {
            "name" : "amount",
            "type" : "Decimal"
          }, {
            "name" : "isoCode",
            "type" : "String"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "CalloutException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Cases" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Cases",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Id",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "emailThreadId",
            "type" : "String"
          } ],
          "name" : "getCaseIdFromEmailThreadId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Communities" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Communities",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "communitiesLanding",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "communitiesLanding",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "forwardToAuthPage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCSS",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "internalLogin",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          }, {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "login",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Comparable" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Integer",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Object"
          } ],
          "name" : "compareTo",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Cookie" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDomain",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMaxAge",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPath",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getValue",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isSecure",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Crypto" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Crypto",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "secretKey",
            "type" : "Blob"
          }, {
            "name" : "initializationVector",
            "type" : "Blob"
          }, {
            "name" : "encryptedData",
            "type" : "Blob"
          } ],
          "name" : "decrypt",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "secretKey",
            "type" : "Blob"
          }, {
            "name" : "encryptedData",
            "type" : "Blob"
          } ],
          "name" : "decryptWithManagedIV",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "secretKey",
            "type" : "Blob"
          }, {
            "name" : "initializationVector",
            "type" : "Blob"
          }, {
            "name" : "clearData",
            "type" : "Blob"
          } ],
          "name" : "encrypt",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "secretKey",
            "type" : "Blob"
          }, {
            "name" : "clearData",
            "type" : "Blob"
          } ],
          "name" : "encryptWithManagedIV",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "size",
            "type" : "Integer"
          } ],
          "name" : "generateAesKey",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "input",
            "type" : "Blob"
          } ],
          "name" : "generateDigest",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "input",
            "type" : "Blob"
          }, {
            "name" : "privateKey",
            "type" : "Blob"
          } ],
          "name" : "generateMac",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRandomInteger",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRandomLong",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ "String", "Blob", "Blob" ],
          "parameters" : [ {
            "name" : "algorithmName",
            "type" : "String"
          }, {
            "name" : "input",
            "type" : "Blob"
          }, {
            "name" : "privateKey",
            "type" : "Blob"
          } ],
          "name" : "sign",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Database" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Database.LeadConvertResult",
          "argTypes" : [ "Database.LeadConvert" ],
          "parameters" : [ {
            "name" : "leadConvert",
            "type" : "Database.LeadConvert"
          } ],
          "name" : "convertLead",
          "references" : [ ]
        }, {
          "returnType" : "Database.LeadConvertResult",
          "argTypes" : [ "Database.LeadConvert", "Boolean" ],
          "parameters" : [ {
            "name" : "leadConvert",
            "type" : "Database.LeadConvert"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "convertLead",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.LeadConvertResult>",
          "argTypes" : [ "LIST<Database.LeadConvert>" ],
          "parameters" : [ {
            "name" : "leadConverts",
            "type" : "LIST<Database.LeadConvert>"
          } ],
          "name" : "convertLead",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.LeadConvertResult>",
          "argTypes" : [ "LIST<Database.LeadConvert>", "Boolean" ],
          "parameters" : [ {
            "name" : "leadConverts",
            "type" : "LIST<Database.LeadConvert>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "convertLead",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "query",
            "type" : "String"
          } ],
          "name" : "countQuery",
          "references" : [ ]
        }, {
          "returnType" : "Database.DeleteResult",
          "argTypes" : [ "Id" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "Database.DeleteResult",
          "argTypes" : [ "Id", "Boolean" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.DeleteResult>",
          "argTypes" : [ "LIST<Id>" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST<Id>"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.DeleteResult>",
          "argTypes" : [ "LIST<Id>", "Boolean" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST<Id>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.DeleteResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.DeleteResult>",
          "argTypes" : [ "LIST<SObject>", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "Database.DeleteResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "Database.DeleteResult",
          "argTypes" : [ "SObject", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "delete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.EmptyRecycleBinResult>",
          "argTypes" : [ "LIST<Id>" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST<Id>"
          } ],
          "name" : "emptyRecycleBin",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.EmptyRecycleBinResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "emptyRecycleBin",
          "references" : [ ]
        }, {
          "returnType" : "Database.EmptyRecycleBinResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "emptyRecycleBin",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "batchable",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "executeBatch",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "APEX_OBJECT", "Integer" ],
          "parameters" : [ {
            "name" : "batchable",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "batchSize",
            "type" : "Integer"
          } ],
          "name" : "executeBatch",
          "references" : [ ]
        }, {
          "returnType" : "Database.QueryLocator",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "query",
            "type" : "LIST<SObject>"
          } ],
          "name" : "getQueryLocator",
          "references" : [ ]
        }, {
          "returnType" : "Database.QueryLocator",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "query",
            "type" : "String"
          } ],
          "name" : "getQueryLocator",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "DmlOptions",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "DmlOptions",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "insert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "query",
            "type" : "String"
          } ],
          "name" : "query",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "System.Savepoint" ],
          "parameters" : [ {
            "name" : "savepoint",
            "type" : "System.Savepoint"
          } ],
          "name" : "rollback",
          "references" : [ ]
        }, {
          "returnType" : "System.Savepoint",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "setSavepoint",
          "references" : [ ]
        }, {
          "returnType" : "Database.UndeleteResult",
          "argTypes" : [ "Id" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "Database.UndeleteResult",
          "argTypes" : [ "Id", "Boolean" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UndeleteResult>",
          "argTypes" : [ "LIST<Id>" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST<Id>"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UndeleteResult>",
          "argTypes" : [ "LIST<Id>", "Boolean" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST<Id>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UndeleteResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UndeleteResult>",
          "argTypes" : [ "LIST<SObject>", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "Database.UndeleteResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "Database.UndeleteResult",
          "argTypes" : [ "SObject", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "undelete",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.SaveResult>",
          "argTypes" : [ "LIST<SObject>", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "Database.SaveResult",
          "argTypes" : [ "SObject", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "update",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UpsertResult>",
          "argTypes" : [ "LIST<SObject>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UpsertResult>",
          "argTypes" : [ "LIST<SObject>", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UpsertResult>",
          "argTypes" : [ "LIST<SObject>", "Schema.SObjectField" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "field",
            "type" : "Schema.SObjectField"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Database.UpsertResult>",
          "argTypes" : [ "LIST<SObject>", "Schema.SObjectField", "Boolean" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<SObject>"
          }, {
            "name" : "field",
            "type" : "Schema.SObjectField"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "Database.UpsertResult",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "Database.UpsertResult",
          "argTypes" : [ "SObject", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "Database.UpsertResult",
          "argTypes" : [ "SObject", "Schema.SObjectField" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "field",
            "type" : "Schema.SObjectField"
          } ],
          "name" : "upsert",
          "references" : [ ]
        }, {
          "returnType" : "Database.UpsertResult",
          "argTypes" : [ "SObject", "Schema.SObjectField", "Boolean" ],
          "parameters" : [ {
            "name" : "sobject",
            "type" : "SObject"
          }, {
            "name" : "field",
            "type" : "Schema.SObjectField"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "upsert",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Date" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Date",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "days",
            "type" : "Integer"
          } ],
          "name" : "addDays",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "months",
            "type" : "Integer"
          } ],
          "name" : "addMonths",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "years",
            "type" : "Integer"
          } ],
          "name" : "addYears",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "day",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "dayOfYear",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "Date"
          } ],
          "name" : "daysBetween",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          } ],
          "name" : "daysInMonth",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          } ],
          "name" : "isLeapYear",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "Date"
          } ],
          "name" : "isSameDay",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "month",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "Date"
          } ],
          "name" : "monthsBetween",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          }, {
            "name" : "day",
            "type" : "Integer"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "parse",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toStartOfMonth",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toStartOfWeek",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "today",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "year",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Datetime" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "days",
            "type" : "Integer"
          } ],
          "name" : "addDays",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "hours",
            "type" : "Integer"
          } ],
          "name" : "addHours",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "minutes",
            "type" : "Integer"
          } ],
          "name" : "addMinutes",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "months",
            "type" : "Integer"
          } ],
          "name" : "addMonths",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "seconds",
            "type" : "Integer"
          } ],
          "name" : "addSeconds",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "years",
            "type" : "Integer"
          } ],
          "name" : "addYears",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "date",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "dateGmt",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "day",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "dayGmt",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "dayOfYear",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "dayOfYearGmt",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "dateformat",
            "type" : "String"
          } ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "dateformat",
            "type" : "String"
          }, {
            "name" : "timezone",
            "type" : "String"
          } ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "dateformat",
            "type" : "String"
          } ],
          "name" : "formatGmt",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "formatLong",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTime",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hour",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hourGmt",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Datetime" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "Datetime"
          } ],
          "name" : "isSameDay",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "millisecond",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "millisecondGmt",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "minute",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "minuteGmt",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "month",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "monthGmt",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Date", "Time" ],
          "parameters" : [ {
            "name" : "date",
            "type" : "Date"
          }, {
            "name" : "time",
            "type" : "Time"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          }, {
            "name" : "day",
            "type" : "Integer"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer", "Integer", "Integer", "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          }, {
            "name" : "day",
            "type" : "Integer"
          }, {
            "name" : "hour",
            "type" : "Integer"
          }, {
            "name" : "minute",
            "type" : "Integer"
          }, {
            "name" : "second",
            "type" : "Integer"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Long" ],
          "parameters" : [ {
            "name" : "time",
            "type" : "Long"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Date", "Time" ],
          "parameters" : [ {
            "name" : "date",
            "type" : "Date"
          }, {
            "name" : "time",
            "type" : "Time"
          } ],
          "name" : "newInstanceGmt",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          }, {
            "name" : "day",
            "type" : "Integer"
          } ],
          "name" : "newInstanceGmt",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Integer", "Integer", "Integer", "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "year",
            "type" : "Integer"
          }, {
            "name" : "month",
            "type" : "Integer"
          }, {
            "name" : "day",
            "type" : "Integer"
          }, {
            "name" : "hour",
            "type" : "Integer"
          }, {
            "name" : "minute",
            "type" : "Integer"
          }, {
            "name" : "second",
            "type" : "Integer"
          } ],
          "name" : "newInstanceGmt",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "now",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "parse",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "second",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "secondGmt",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "time",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "timeGmt",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOfGmt",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "year",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "yearGmt",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Decimal" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Decimal",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "abs",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal", "Integer" ],
          "parameters" : [ {
            "name" : "divisor",
            "type" : "Decimal"
          }, {
            "name" : "scale",
            "type" : "Integer"
          } ],
          "name" : "divide",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal", "Integer", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "divisor",
            "type" : "Decimal"
          }, {
            "name" : "scale",
            "type" : "Integer"
          }, {
            "name" : "roundingMode",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "divide",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "doubleValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "intValue",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "longValue",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "exponent",
            "type" : "Integer"
          } ],
          "name" : "pow",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "precision",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "round",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "system.RoundingMode" ],
          "parameters" : [ {
            "name" : "roundingMode",
            "type" : "system.RoundingMode"
          } ],
          "name" : "round",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "scale",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "scale",
            "type" : "Integer"
          } ],
          "name" : "setScale",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Integer", "system.RoundingMode" ],
          "parameters" : [ {
            "name" : "scale",
            "type" : "Integer"
          }, {
            "name" : "roundingMode",
            "type" : "system.RoundingMode"
          } ],
          "name" : "setScale",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "stripTrailingZeros",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toPlainString",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "dbl",
            "type" : "Double"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Long" ],
          "parameters" : [ {
            "name" : "lng",
            "type" : "Long"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "DmlException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlFieldNames",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Schema.SObjectField>",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlFields",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlId",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlIndex",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlStatusCode",
          "references" : [ ]
        }, {
          "returnType" : "system.StatusCode",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlType",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNumDml",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Double" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "intValue",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "longValue",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "round",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "EmailException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlFieldNames",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Schema.SObjectField>",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlFields",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlId",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlIndex",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlStatusCode",
          "references" : [ ]
        }, {
          "returnType" : "system.StatusCode",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getDmlType",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNumDml",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "EncodingUtil" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "EncodingUtil",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Blob",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          } ],
          "name" : "base64Decode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Blob" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "Blob"
          } ],
          "name" : "base64Encode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Blob" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "Blob"
          } ],
          "name" : "convertToHex",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          }, {
            "name" : "enc",
            "type" : "String"
          } ],
          "name" : "urlDecode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          }, {
            "name" : "enc",
            "type" : "String"
          } ],
          "name" : "urlEncode",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Exception" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FinalException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "FlowException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "HandledException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Http" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "System.HttpResponse",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "request",
            "type" : "ANY"
          } ],
          "name" : "send",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "HttpCalloutMock" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "System.HttpResponse",
          "argTypes" : [ "System.HttpRequest" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "System.HttpRequest"
          } ],
          "name" : "respond",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "HttpRequest" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBody",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBodyAsBlob",
          "references" : [ ]
        }, {
          "returnType" : "dom.Document",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBodyDocument",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCompressed",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getEndpoint",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          } ],
          "name" : "getHeader",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMethod",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "body",
            "type" : "String"
          } ],
          "name" : "setBody",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Blob" ],
          "parameters" : [ {
            "name" : "body",
            "type" : "Blob"
          } ],
          "name" : "setBodyAsBlob",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "body",
            "type" : "ANY"
          } ],
          "name" : "setBodyDocument",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "clientCert",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "setClientCertificate",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "certDevName",
            "type" : "String"
          } ],
          "name" : "setClientCertificateName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "compressed",
            "type" : "Boolean"
          } ],
          "name" : "setCompressed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "endpoint",
            "type" : "String"
          } ],
          "name" : "setEndpoint",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "setHeader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "method",
            "type" : "String"
          } ],
          "name" : "setMethod",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "timeout",
            "type" : "Integer"
          } ],
          "name" : "setTimeout",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "HttpResponse" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBody",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBodyAsBlob",
          "references" : [ ]
        }, {
          "returnType" : "dom.Document",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBodyDocument",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          } ],
          "name" : "getHeader",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHeaderKeys",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStatus",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStatusCode",
          "references" : [ ]
        }, {
          "returnType" : "System.XmlStreamReader",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getXmlStreamReader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "body",
            "type" : "String"
          } ],
          "name" : "setBody",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Blob" ],
          "parameters" : [ {
            "name" : "body",
            "type" : "Blob"
          } ],
          "name" : "setBodyAsBlob",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "setHeader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "status",
            "type" : "String"
          } ],
          "name" : "setStatus",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "statusCode",
            "type" : "Integer"
          } ],
          "name" : "setStatusCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Id" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Schema.SObjectType",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSobjectType",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Ideas" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Ideas",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "SObject" ],
          "parameters" : [ {
            "name" : "idea",
            "type" : "SObject"
          } ],
          "name" : "findSimilar",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getAllRecentReplies",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getReadRecentReplies",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "userId",
            "type" : "String"
          }, {
            "name" : "communityId",
            "type" : "String"
          } ],
          "name" : "getUnreadRecentReplies",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "ideaId",
            "type" : "String"
          } ],
          "name" : "markRead",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Integer" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "i",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "InvalidHeaderException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "InvalidHeaderException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "Exception"
          } ],
          "name" : "InvalidHeaderException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          } ],
          "name" : "InvalidHeaderException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          }, {
            "name" : "param2",
            "type" : "Exception"
          } ],
          "name" : "InvalidHeaderException",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "InvalidParameterValueException" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          }, {
            "name" : "param2",
            "type" : "String"
          } ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "InvalidReadOnlyUserDmlException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Iterable" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "system.Iterator",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "iterator",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Iterator" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasNext",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "JSON" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "JSON",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "system.JSONGenerator",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "pretty",
            "type" : "Boolean"
          } ],
          "name" : "createGenerator",
          "references" : [ ]
        }, {
          "returnType" : "system.JSONParser",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "jsonString",
            "type" : "String"
          } ],
          "name" : "createParser",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "String", "system.Type" ],
          "parameters" : [ {
            "name" : "jsonString",
            "type" : "String"
          }, {
            "name" : "apexType",
            "type" : "system.Type"
          } ],
          "name" : "deserialize",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "String", "system.Type" ],
          "parameters" : [ {
            "name" : "jsonString",
            "type" : "String"
          }, {
            "name" : "apexType",
            "type" : "system.Type"
          } ],
          "name" : "deserializeStrict",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "jsonString",
            "type" : "String"
          } ],
          "name" : "deserializeUntyped",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "serialize",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "serializePretty",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "JSONException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "JSONGenerator" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "close",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAsString",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isClosed",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Blob" ],
          "parameters" : [ {
            "name" : "b",
            "type" : "Blob"
          } ],
          "name" : "writeBlob",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Blob" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "b",
            "type" : "Blob"
          } ],
          "name" : "writeBlobField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "b",
            "type" : "Boolean"
          } ],
          "name" : "writeBoolean",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "b",
            "type" : "Boolean"
          } ],
          "name" : "writeBooleanField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Date"
          } ],
          "name" : "writeDate",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Date" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "d",
            "type" : "Date"
          } ],
          "name" : "writeDateField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Datetime" ],
          "parameters" : [ {
            "name" : "dt",
            "type" : "Datetime"
          } ],
          "name" : "writeDateTime",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Datetime" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "dt",
            "type" : "Datetime"
          } ],
          "name" : "writeDateTimeField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeEndArray",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeEndObject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          } ],
          "name" : "writeFieldName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Id" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "Id"
          } ],
          "name" : "writeId",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Id" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "id",
            "type" : "Id"
          } ],
          "name" : "writeIdField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeNull",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          } ],
          "name" : "writeNullField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Decimal"
          } ],
          "name" : "writeNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Double"
          } ],
          "name" : "writeNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "i",
            "type" : "Integer"
          } ],
          "name" : "writeNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Long" ],
          "parameters" : [ {
            "name" : "lng",
            "type" : "Long"
          } ],
          "name" : "writeNumber",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Decimal" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "d",
            "type" : "Decimal"
          } ],
          "name" : "writeNumberField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Double" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "d",
            "type" : "Double"
          } ],
          "name" : "writeNumberField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "i",
            "type" : "Integer"
          } ],
          "name" : "writeNumberField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Long" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "lng",
            "type" : "Long"
          } ],
          "name" : "writeNumberField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "writeObject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Object" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "writeObjectField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeStartArray",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeStartObject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "writeString",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "writeStringField",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Time" ],
          "parameters" : [ {
            "name" : "t",
            "type" : "Time"
          } ],
          "name" : "writeTime",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Time" ],
          "parameters" : [ {
            "name" : "fieldName",
            "type" : "String"
          }, {
            "name" : "t",
            "type" : "Time"
          } ],
          "name" : "writeTimeField",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "JSONParser" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clearCurrentToken",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBlobValue",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getBooleanValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCurrentName",
          "references" : [ ]
        }, {
          "returnType" : "system.JSONToken",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCurrentToken",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDateTimeValue",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDateValue",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDecimalValue",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDoubleValue",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getIdValue",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getIntegerValue",
          "references" : [ ]
        }, {
          "returnType" : "system.JSONToken",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLastClearedToken",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLongValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getText",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTimeValue",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasCurrentToken",
          "references" : [ ]
        }, {
          "returnType" : "system.JSONToken",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "nextToken",
          "references" : [ ]
        }, {
          "returnType" : "system.JSONToken",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "nextValue",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "system.Type" ],
          "parameters" : [ {
            "name" : "apexType",
            "type" : "system.Type"
          } ],
          "name" : "readValueAs",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "system.Type" ],
          "parameters" : [ {
            "name" : "apexType",
            "type" : "system.Type"
          } ],
          "name" : "readValueAsStrict",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "skipChildren",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "JSONToken" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.JSONToken>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "END_ARRAY",
          "references" : [ ]
        }, {
          "name" : "END_OBJECT",
          "references" : [ ]
        }, {
          "name" : "FIELD_NAME",
          "references" : [ ]
        }, {
          "name" : "NOT_AVAILABLE",
          "references" : [ ]
        }, {
          "name" : "START_ARRAY",
          "references" : [ ]
        }, {
          "name" : "START_OBJECT",
          "references" : [ ]
        }, {
          "name" : "VALUE_EMBEDDED_OBJECT",
          "references" : [ ]
        }, {
          "name" : "VALUE_FALSE",
          "references" : [ ]
        }, {
          "name" : "VALUE_NULL",
          "references" : [ ]
        }, {
          "name" : "VALUE_NUMBER_FLOAT",
          "references" : [ ]
        }, {
          "name" : "VALUE_NUMBER_INT",
          "references" : [ ]
        }, {
          "name" : "VALUE_STRING",
          "references" : [ ]
        }, {
          "name" : "VALUE_TRUE",
          "references" : [ ]
        } ]
      },
      "LIST" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Object",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "element",
            "type" : "ANY"
          } ],
          "name" : "add",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer", "ANY" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          }, {
            "name" : "element",
            "type" : "ANY"
          } ],
          "name" : "add",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "LIST"
          } ],
          "name" : "addAll",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "SET" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "SET"
          } ],
          "name" : "addAll",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clear",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "deepClone",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          } ],
          "name" : "deepClone",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "Boolean", "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          }, {
            "name" : "preserveReadOnlyTimestamps",
            "type" : "Boolean"
          } ],
          "name" : "deepClone",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "Boolean", "Boolean", "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          }, {
            "name" : "preserveReadOnlyTimestamps",
            "type" : "Boolean"
          }, {
            "name" : "preserveAutoNumbers",
            "type" : "Boolean"
          } ],
          "name" : "deepClone",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "get",
          "references" : [ ]
        }, {
          "returnType" : "Schema.SObjectType",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSObjectType",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isEmpty",
          "references" : [ ]
        }, {
          "returnType" : "system.ListIterator",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "iterator",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "remove",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer", "ANY" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          }, {
            "name" : "value",
            "type" : "ANY"
          } ],
          "name" : "set",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "size",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "sort",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "LicenseException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "LimitException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ListException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "LoggingLevel" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.LoggingLevel>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "DEBUG",
          "references" : [ ]
        }, {
          "name" : "ERROR",
          "references" : [ ]
        }, {
          "name" : "FINE",
          "references" : [ ]
        }, {
          "name" : "FINER",
          "references" : [ ]
        }, {
          "name" : "FINEST",
          "references" : [ ]
        }, {
          "name" : "INFO",
          "references" : [ ]
        }, {
          "name" : "INTERNAL",
          "references" : [ ]
        }, {
          "name" : "WARN",
          "references" : [ ]
        } ]
      },
      "Long" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "intValue",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Map" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clear",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "ANY"
          } ],
          "name" : "containsKey",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "deepClone",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "ANY"
          } ],
          "name" : "get",
          "references" : [ ]
        }, {
          "returnType" : "Schema.SObjectType",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSObjectType",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isEmpty",
          "references" : [ ]
        }, {
          "returnType" : "SET<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "keySet",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "ANY", "ANY" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "ANY"
          }, {
            "name" : "value",
            "type" : "ANY"
          } ],
          "name" : "put",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "entries",
            "type" : "LIST"
          } ],
          "name" : "putAll",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "MAP" ],
          "parameters" : [ {
            "name" : "entries",
            "type" : "MAP"
          } ],
          "name" : "putAll",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "ANY"
          } ],
          "name" : "remove",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "size",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Matcher" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "end",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "grp",
            "type" : "Integer"
          } ],
          "name" : "end",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "find",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "start",
            "type" : "Integer"
          } ],
          "name" : "find",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "group",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "start",
            "type" : "Integer"
          } ],
          "name" : "group",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "groupCount",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasAnchoringBounds",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasTransparentBounds",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hitEnd",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "lookingAt",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "matches",
          "references" : [ ]
        }, {
          "returnType" : "system.Pattern",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "pattern",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          } ],
          "name" : "quoteReplacement",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "start",
            "type" : "Integer"
          }, {
            "name" : "ending",
            "type" : "Integer"
          } ],
          "name" : "region",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "regionEnd",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "regionStart",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "replacement",
            "type" : "String"
          } ],
          "name" : "replaceAll",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "replacement",
            "type" : "String"
          } ],
          "name" : "replaceFirst",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "requireEnd",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "input",
            "type" : "String"
          } ],
          "name" : "reset",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "start",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "grp",
            "type" : "Integer"
          } ],
          "name" : "start",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "b",
            "type" : "Boolean"
          } ],
          "name" : "useAnchoringBounds",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "system.Pattern" ],
          "parameters" : [ {
            "name" : "p",
            "type" : "system.Pattern"
          } ],
          "name" : "usePattern",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "b",
            "type" : "Boolean"
          } ],
          "name" : "useTransparentBounds",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Math" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Math",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "abs",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "abs",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Integer"
          } ],
          "name" : "abs",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Long" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Long"
          } ],
          "name" : "abs",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "acos",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "acos",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "asin",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "asin",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "atan",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "atan",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal", "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          }, {
            "name" : "y",
            "type" : "Decimal"
          } ],
          "name" : "atan2",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double", "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          }, {
            "name" : "y",
            "type" : "Double"
          } ],
          "name" : "atan2",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "cbrt",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "cbrt",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "ceil",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "ceil",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "cos",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "cos",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "cosh",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "cosh",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "exp",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "exp",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "floor",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "floor",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "log",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "log",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "log10",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "log10",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal", "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          }, {
            "name" : "y",
            "type" : "Decimal"
          } ],
          "name" : "max",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double", "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          }, {
            "name" : "y",
            "type" : "Double"
          } ],
          "name" : "max",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Integer"
          }, {
            "name" : "y",
            "type" : "Integer"
          } ],
          "name" : "max",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Long", "Long" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Long"
          }, {
            "name" : "y",
            "type" : "Long"
          } ],
          "name" : "max",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal", "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          }, {
            "name" : "y",
            "type" : "Decimal"
          } ],
          "name" : "min",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double", "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          }, {
            "name" : "y",
            "type" : "Double"
          } ],
          "name" : "min",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Integer"
          }, {
            "name" : "y",
            "type" : "Integer"
          } ],
          "name" : "min",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Long", "Long" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Long"
          }, {
            "name" : "y",
            "type" : "Long"
          } ],
          "name" : "min",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Integer"
          }, {
            "name" : "y",
            "type" : "Integer"
          } ],
          "name" : "mod",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Long", "Long" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Long"
          }, {
            "name" : "y",
            "type" : "Long"
          } ],
          "name" : "mod",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double", "Double" ],
          "parameters" : [ {
            "name" : "base",
            "type" : "Double"
          }, {
            "name" : "exp",
            "type" : "Double"
          } ],
          "name" : "pow",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "random",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "rint",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "rint",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "round",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "round",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "roundToLong",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "roundToLong",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "signum",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "signum",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "sin",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "sin",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "sinh",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "sinh",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "sqrt",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "sqrt",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "tan",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "tan",
          "references" : [ ]
        }, {
          "returnType" : "Decimal",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Decimal"
          } ],
          "name" : "tanh",
          "references" : [ ]
        }, {
          "returnType" : "Double",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "x",
            "type" : "Double"
          } ],
          "name" : "tanh",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "MathException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Messaging" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "count",
            "type" : "Integer"
          } ],
          "name" : "reserveMassEmailCapacity",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "count",
            "type" : "Integer"
          } ],
          "name" : "reserveSingleEmailCapacity",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Messaging.SendEmailResult>",
          "argTypes" : [ "LIST<Messaging.Email>" ],
          "parameters" : [ {
            "name" : "emailMessages",
            "type" : "LIST<Messaging.Email>"
          } ],
          "name" : "sendEmail",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Messaging.SendEmailResult>",
          "argTypes" : [ "LIST<Messaging.Email>", "Boolean" ],
          "parameters" : [ {
            "name" : "emailMessages",
            "type" : "LIST<Messaging.Email>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "sendEmail",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Messaging.SendEmailResult>",
          "argTypes" : [ "LIST<Id>" ],
          "parameters" : [ {
            "name" : "emailMessagesIds",
            "type" : "LIST<Id>"
          } ],
          "name" : "sendEmailMessage",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Messaging.SendEmailResult>",
          "argTypes" : [ "LIST<Id>", "Boolean" ],
          "parameters" : [ {
            "name" : "emailMessagesIds",
            "type" : "LIST<Id>"
          }, {
            "name" : "allOrNothing",
            "type" : "Boolean"
          } ],
          "name" : "sendEmailMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "MultiStaticResourceCalloutMock" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "MultiStaticResourceCalloutMock",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "System.HttpResponse",
          "argTypes" : [ "System.HttpRequest" ],
          "parameters" : [ {
            "name" : "request",
            "type" : "System.HttpRequest"
          } ],
          "name" : "respond",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "val",
            "type" : "String"
          } ],
          "name" : "setHeader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "url",
            "type" : "String"
          }, {
            "name" : "staticResourceName",
            "type" : "String"
          } ],
          "name" : "setStaticResource",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "status",
            "type" : "String"
          } ],
          "name" : "setStatus",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "code",
            "type" : "Integer"
          } ],
          "name" : "setStatusCode",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Network" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Network",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "communitiesLanding",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "forwardToAuthPage",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "startUrl",
            "type" : "String"
          }, {
            "name" : "displayType",
            "type" : "String"
          } ],
          "name" : "forwardToAuthPage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNetworkId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "NoAccessException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "NoDataFoundException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "NoSuchElementException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "NullPointerException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "PageReference" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAnchor",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getContent",
          "references" : [ ]
        }, {
          "returnType" : "Blob",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getContentAsPDF",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,System.Cookie>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCookies",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHeaders",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getParameters",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRedirect",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUrl",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "anchor",
            "type" : "String"
          } ],
          "name" : "setAnchor",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST<System.Cookie>" ],
          "parameters" : [ {
            "name" : "cookies",
            "type" : "LIST<System.Cookie>"
          } ],
          "name" : "setCookies",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "redirect",
            "type" : "Boolean"
          } ],
          "name" : "setRedirect",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Pattern" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "system.Pattern",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          } ],
          "name" : "compile",
          "references" : [ ]
        }, {
          "returnType" : "system.Matcher",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "input",
            "type" : "String"
          } ],
          "name" : "matcher",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          }, {
            "name" : "input",
            "type" : "String"
          } ],
          "name" : "matches",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "pattern",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          } ],
          "name" : "quote",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "input",
            "type" : "String"
          } ],
          "name" : "split",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "input",
            "type" : "String"
          }, {
            "name" : "n",
            "type" : "Integer"
          } ],
          "name" : "split",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "ProcedureException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "QueryException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "RequiredFeatureMissingException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "RestContext" : {
        "constructors" : [ ],
        "methods" : [ ],
        "properties" : [ {
          "name" : "request",
          "references" : [ ]
        }, {
          "name" : "response",
          "references" : [ ]
        } ]
      },
      "RestRequest" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "RestRequest",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "addHeader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "addParameter",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "headers",
          "references" : [ ]
        }, {
          "name" : "httpMethod",
          "references" : [ ]
        }, {
          "name" : "params",
          "references" : [ ]
        }, {
          "name" : "remoteAddress",
          "references" : [ ]
        }, {
          "name" : "requestBody",
          "references" : [ ]
        }, {
          "name" : "requestURI",
          "references" : [ ]
        }, {
          "name" : "resourcePath",
          "references" : [ ]
        } ]
      },
      "RestResponse" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "RestResponse",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "addHeader",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "headers",
          "references" : [ ]
        }, {
          "name" : "responseBody",
          "references" : [ ]
        }, {
          "name" : "statusCode",
          "references" : [ ]
        } ]
      },
      "SObject" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clear",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          } ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Boolean", "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          }, {
            "name" : "deep",
            "type" : "Boolean"
          } ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Boolean", "Boolean", "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          }, {
            "name" : "deep",
            "type" : "Boolean"
          }, {
            "name" : "preserveReadOnlyTimestamps",
            "type" : "Boolean"
          } ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Boolean", "Boolean", "Boolean", "Boolean" ],
          "parameters" : [ {
            "name" : "preserveId",
            "type" : "Boolean"
          }, {
            "name" : "deep",
            "type" : "Boolean"
          }, {
            "name" : "preserveReadOnlyTimestamps",
            "type" : "Boolean"
          }, {
            "name" : "preserveAutoNumbers",
            "type" : "Boolean"
          } ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "Schema.SObjectField" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "Schema.SObjectField"
          } ],
          "name" : "get",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "String"
          } ],
          "name" : "get",
          "references" : [ ]
        }, {
          "returnType" : "Database.DMLOptions",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getOptions",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getQuickActionName",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Schema.SObjectField" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "Schema.SObjectField"
          } ],
          "name" : "getSObject",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "String"
          } ],
          "name" : "getSObject",
          "references" : [ ]
        }, {
          "returnType" : "Schema.SObjectType",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSObjectType",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ "Schema.SObjectField" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "Schema.SObjectField"
          } ],
          "name" : "getSObjects",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "String"
          } ],
          "name" : "getSObjects",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "Schema.SObjectField", "Object" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "Schema.SObjectField"
          }, {
            "name" : "value",
            "type" : "Object"
          } ],
          "name" : "put",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ "String", "Object" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "Object"
          } ],
          "name" : "put",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "Schema.SObjectField", "SObject" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "Schema.SObjectField"
          }, {
            "name" : "value",
            "type" : "SObject"
          } ],
          "name" : "putSObject",
          "references" : [ ]
        }, {
          "returnType" : "SObject",
          "argTypes" : [ "String", "SObject" ],
          "parameters" : [ {
            "name" : "field",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "SObject"
          } ],
          "name" : "putSObject",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "options",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "setOptions",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SObjectException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Schedulable" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "system.SchedulableContext" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "system.SchedulableContext"
          } ],
          "name" : "execute",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SchedulableContext" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTriggerId",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Schema" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<Schema.DescribeDataCategoryGroupStructureResult>",
          "argTypes" : [ "LIST<Schema.DataCategoryGroupSobjectTypePair>", "Boolean" ],
          "parameters" : [ {
            "name" : "pairs",
            "type" : "LIST<Schema.DataCategoryGroupSobjectTypePair>"
          }, {
            "name" : "topCategoriesOnly",
            "type" : "Boolean"
          } ],
          "name" : "describeDataCategoryGroupStructures",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Schema.DescribeDataCategoryGroupResult>",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "sobjects",
            "type" : "LIST<String>"
          } ],
          "name" : "describeDataCategoryGroups",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,Schema.SObjectType>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "appName",
            "type" : "String"
          } ],
          "name" : "getAppDescribe",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,Schema.SObjectType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getGlobalDescribe",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,Schema.SObjectType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getModuleDescribe",
          "references" : [ ]
        }, {
          "returnType" : "MAP<String,Schema.SObjectType>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "moduleName",
            "type" : "String"
          } ],
          "name" : "getModuleDescribe",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SearchException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SecurityException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SelectOption" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDisabled",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getEscapeItem",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLabel",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getValue",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "disabled",
            "type" : "Boolean"
          } ],
          "name" : "setDisabled",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "disabled",
            "type" : "Boolean"
          } ],
          "name" : "setEscapeItem",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "label",
            "type" : "String"
          } ],
          "name" : "setLabel",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "setValue",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SerializationException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Set" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "element",
            "type" : "ANY"
          } ],
          "name" : "add",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "LIST"
          } ],
          "name" : "addAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "SET" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "SET"
          } ],
          "name" : "addAll",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clear",
          "references" : [ ]
        }, {
          "returnType" : "SET<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "clone",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "element",
            "type" : "ANY"
          } ],
          "name" : "contains",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "LIST"
          } ],
          "name" : "containsAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "SET" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "SET"
          } ],
          "name" : "containsAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isEmpty",
          "references" : [ ]
        }, {
          "returnType" : "system.ListIterator",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "iterator",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "element",
            "type" : "ANY"
          } ],
          "name" : "remove",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "LIST"
          } ],
          "name" : "removeAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "SET" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "SET"
          } ],
          "name" : "removeAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "LIST"
          } ],
          "name" : "retainAll",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "SET" ],
          "parameters" : [ {
            "name" : "elements",
            "type" : "SET"
          } ],
          "name" : "retainAll",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "size",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "SetupScope" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.SetupScope>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ORGANIZATION",
          "references" : [ ]
        }, {
          "name" : "PROFILE",
          "references" : [ ]
        }, {
          "name" : "USER",
          "references" : [ ]
        } ]
      },
      "Site" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Site",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "newPassword",
            "type" : "String"
          }, {
            "name" : "verifyNewPassword",
            "type" : "String"
          } ],
          "name" : "changePassword",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "newPassword",
            "type" : "String"
          }, {
            "name" : "verifyNewPassword",
            "type" : "String"
          }, {
            "name" : "oldPassword",
            "type" : "String"
          } ],
          "name" : "changePassword",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "ownerId",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "createPersonAccountPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "ownerId",
            "type" : "String"
          }, {
            "name" : "recordTypeId",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "createPersonAccountPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "accountId",
            "type" : "String"
          } ],
          "name" : "createPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "accountId",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "createPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ "SObject", "String", "String", "Boolean" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "accountId",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          }, {
            "name" : "sendEmailConfirmation",
            "type" : "Boolean"
          } ],
          "name" : "createPortalUser",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          } ],
          "name" : "forgotPassword",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAdminEmail",
          "references" : [ ]
        }, {
          "returnType" : "Id",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAdminId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAnalyticsTrackingCode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCurrentSiteUrl",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCustomWebAddress",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDomain",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getErrorDescription",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getErrorMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getOriginalUrl",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPrefix",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTemplate",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isLoginEnabled",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isPasswordExpired",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isRegistrationEnabled",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "username",
            "type" : "String"
          }, {
            "name" : "password",
            "type" : "String"
          }, {
            "name" : "startUrl",
            "type" : "String"
          } ],
          "name" : "login",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "SObject", "String" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "accountId",
            "type" : "String"
          } ],
          "name" : "setPortalUserAsAuthProvider",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "StaticResourceCalloutMock" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "StaticResourceCalloutMock",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "System.HttpResponse",
          "argTypes" : [ "System.HttpRequest" ],
          "parameters" : [ {
            "name" : "request",
            "type" : "System.HttpRequest"
          } ],
          "name" : "respond",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "val",
            "type" : "String"
          } ],
          "name" : "setHeader",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "staticResourceName",
            "type" : "String"
          } ],
          "name" : "setStaticResource",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "status",
            "type" : "String"
          } ],
          "name" : "setStatus",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "code",
            "type" : "Integer"
          } ],
          "name" : "setStatusCode",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "StatusCode" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.StatusCode>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ALL_OR_NONE_OPERATION_ROLLED_BACK",
          "references" : [ ]
        }, {
          "name" : "ALREADY_IN_PROCESS",
          "references" : [ ]
        }, {
          "name" : "ASSIGNEE_TYPE_REQUIRED",
          "references" : [ ]
        }, {
          "name" : "BAD_CUSTOM_ENTITY_PARENT_DOMAIN",
          "references" : [ ]
        }, {
          "name" : "BCC_NOT_ALLOWED_IF_BCC_COMPLIANCE_ENABLED",
          "references" : [ ]
        }, {
          "name" : "CANNOT_CASCADE_PRODUCT_ACTIVE",
          "references" : [ ]
        }, {
          "name" : "CANNOT_CHANGE_FIELD_TYPE_OF_APEX_REFERENCED_FIELD",
          "references" : [ ]
        }, {
          "name" : "CANNOT_CHANGE_FIELD_TYPE_OF_REFERENCED_FIELD",
          "references" : [ ]
        }, {
          "name" : "CANNOT_CREATE_ANOTHER_MANAGED_PACKAGE",
          "references" : [ ]
        }, {
          "name" : "CANNOT_DEACTIVATE_DIVISION",
          "references" : [ ]
        }, {
          "name" : "CANNOT_DELETE_LAST_DATED_CONVERSION_RATE",
          "references" : [ ]
        }, {
          "name" : "CANNOT_DELETE_MANAGED_OBJECT",
          "references" : [ ]
        }, {
          "name" : "CANNOT_DISABLE_LAST_ADMIN",
          "references" : [ ]
        }, {
          "name" : "CANNOT_ENABLE_IP_RESTRICT_REQUESTS",
          "references" : [ ]
        }, {
          "name" : "CANNOT_EXECUTE_FLOW_TRIGGER",
          "references" : [ ]
        }, {
          "name" : "CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY",
          "references" : [ ]
        }, {
          "name" : "CANNOT_MODIFY_MANAGED_OBJECT",
          "references" : [ ]
        }, {
          "name" : "CANNOT_RENAME_APEX_REFERENCED_FIELD",
          "references" : [ ]
        }, {
          "name" : "CANNOT_RENAME_APEX_REFERENCED_OBJECT",
          "references" : [ ]
        }, {
          "name" : "CANNOT_RENAME_REFERENCED_FIELD",
          "references" : [ ]
        }, {
          "name" : "CANNOT_RENAME_REFERENCED_OBJECT",
          "references" : [ ]
        }, {
          "name" : "CANNOT_REPARENT_RECORD",
          "references" : [ ]
        }, {
          "name" : "CANNOT_UPDATE_CONVERTED_LEAD",
          "references" : [ ]
        }, {
          "name" : "CANT_DISABLE_CORP_CURRENCY",
          "references" : [ ]
        }, {
          "name" : "CANT_UNSET_CORP_CURRENCY",
          "references" : [ ]
        }, {
          "name" : "CHILD_SHARE_FAILS_PARENT",
          "references" : [ ]
        }, {
          "name" : "CIRCULAR_DEPENDENCY",
          "references" : [ ]
        }, {
          "name" : "COLLISION_DETECTED",
          "references" : [ ]
        }, {
          "name" : "COMMUNITY_NOT_ACCESSIBLE",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_CLOB_FIELD_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_ENTITY_OR_FIELD_LIMIT",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_FIELD_INDEX_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_INDEX_EXISTS",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_LINK_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_METADATA_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "CUSTOM_TAB_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "DELETE_FAILED",
          "references" : [ ]
        }, {
          "name" : "DELETE_OPERATION_TOO_LARGE",
          "references" : [ ]
        }, {
          "name" : "DELETE_REQUIRED_ON_CASCADE",
          "references" : [ ]
        }, {
          "name" : "DEPENDENCY_EXISTS",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_CASE_SOLUTION",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_COMM_NICKNAME",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_CUSTOM_ENTITY_DEFINITION",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_CUSTOM_TAB_MOTIF",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_DEVELOPER_NAME",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_EXTERNAL_ID",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_MASTER_LABEL",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_SENDER_DISPLAY_NAME",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_USERNAME",
          "references" : [ ]
        }, {
          "name" : "DUPLICATE_VALUE",
          "references" : [ ]
        }, {
          "name" : "EMAIL_NOT_PROCESSED_DUE_TO_PRIOR_ERROR",
          "references" : [ ]
        }, {
          "name" : "EMPTY_SCONTROL_FILE_NAME",
          "references" : [ ]
        }, {
          "name" : "ENTITY_FAILED_IFLASTMODIFIED_ON_UPDATE",
          "references" : [ ]
        }, {
          "name" : "ENTITY_IS_ARCHIVED",
          "references" : [ ]
        }, {
          "name" : "ENTITY_IS_DELETED",
          "references" : [ ]
        }, {
          "name" : "ENTITY_IS_LOCKED",
          "references" : [ ]
        }, {
          "name" : "ENVIRONMENT_HUB_MEMBERSHIP_CONFLICT",
          "references" : [ ]
        }, {
          "name" : "ENVIRONMENT_HUB_MEMBERSHIP_ERROR_JOINING_HUB",
          "references" : [ ]
        }, {
          "name" : "ENVIRONMENT_HUB_MEMBERSHIP_USER_ALREADY_IN_HUB",
          "references" : [ ]
        }, {
          "name" : "ENVIRONMENT_HUB_MEMBERSHIP_USER_NOT_ORG_ADMIN",
          "references" : [ ]
        }, {
          "name" : "ERROR_IN_MAILER",
          "references" : [ ]
        }, {
          "name" : "FAILED_ACTIVATION",
          "references" : [ ]
        }, {
          "name" : "FIELD_CUSTOM_VALIDATION_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "FIELD_FILTER_VALIDATION_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "FIELD_INTEGRITY_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "FILTERED_LOOKUP_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "HTML_FILE_UPLOAD_NOT_ALLOWED",
          "references" : [ ]
        }, {
          "name" : "IMAGE_TOO_LARGE",
          "references" : [ ]
        }, {
          "name" : "INACTIVE_OWNER_OR_USER",
          "references" : [ ]
        }, {
          "name" : "INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY",
          "references" : [ ]
        }, {
          "name" : "INSUFFICIENT_ACCESS_OR_READONLY",
          "references" : [ ]
        }, {
          "name" : "INVALID_ACCESS_LEVEL",
          "references" : [ ]
        }, {
          "name" : "INVALID_ARGUMENT_TYPE",
          "references" : [ ]
        }, {
          "name" : "INVALID_ASSIGNEE_TYPE",
          "references" : [ ]
        }, {
          "name" : "INVALID_ASSIGNMENT_RULE",
          "references" : [ ]
        }, {
          "name" : "INVALID_BATCH_OPERATION",
          "references" : [ ]
        }, {
          "name" : "INVALID_CONTENT_TYPE",
          "references" : [ ]
        }, {
          "name" : "INVALID_CREDIT_CARD_INFO",
          "references" : [ ]
        }, {
          "name" : "INVALID_CROSS_REFERENCE_KEY",
          "references" : [ ]
        }, {
          "name" : "INVALID_CROSS_REFERENCE_TYPE_FOR_FIELD",
          "references" : [ ]
        }, {
          "name" : "INVALID_CURRENCY_CONV_RATE",
          "references" : [ ]
        }, {
          "name" : "INVALID_CURRENCY_CORP_RATE",
          "references" : [ ]
        }, {
          "name" : "INVALID_CURRENCY_ISO",
          "references" : [ ]
        }, {
          "name" : "INVALID_DATA_CATEGORY_GROUP_REFERENCE",
          "references" : [ ]
        }, {
          "name" : "INVALID_DATA_URI",
          "references" : [ ]
        }, {
          "name" : "INVALID_EMAIL_ADDRESS",
          "references" : [ ]
        }, {
          "name" : "INVALID_EMPTY_KEY_OWNER",
          "references" : [ ]
        }, {
          "name" : "INVALID_FIELD",
          "references" : [ ]
        }, {
          "name" : "INVALID_FIELD_FOR_INSERT_UPDATE",
          "references" : [ ]
        }, {
          "name" : "INVALID_FIELD_WHEN_USING_TEMPLATE",
          "references" : [ ]
        }, {
          "name" : "INVALID_FILTER_ACTION",
          "references" : [ ]
        }, {
          "name" : "INVALID_GOOGLE_DOCS_URL",
          "references" : [ ]
        }, {
          "name" : "INVALID_ID_FIELD",
          "references" : [ ]
        }, {
          "name" : "INVALID_INET_ADDRESS",
          "references" : [ ]
        }, {
          "name" : "INVALID_LINEITEM_CLONE_STATE",
          "references" : [ ]
        }, {
          "name" : "INVALID_MASTER_OR_TRANSLATED_SOLUTION",
          "references" : [ ]
        }, {
          "name" : "INVALID_MESSAGE_ID_REFERENCE",
          "references" : [ ]
        }, {
          "name" : "INVALID_OAUTH_URL",
          "references" : [ ]
        }, {
          "name" : "INVALID_OPERATION",
          "references" : [ ]
        }, {
          "name" : "INVALID_OPERATOR",
          "references" : [ ]
        }, {
          "name" : "INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST",
          "references" : [ ]
        }, {
          "name" : "INVALID_OWNER",
          "references" : [ ]
        }, {
          "name" : "INVALID_PACKAGE_VERSION",
          "references" : [ ]
        }, {
          "name" : "INVALID_PARTNER_NETWORK_STATUS",
          "references" : [ ]
        }, {
          "name" : "INVALID_PERSON_ACCOUNT_OPERATION",
          "references" : [ ]
        }, {
          "name" : "INVALID_QUERY_LOCATOR",
          "references" : [ ]
        }, {
          "name" : "INVALID_READ_ONLY_USER_DML",
          "references" : [ ]
        }, {
          "name" : "INVALID_SAVE_AS_ACTIVITY_FLAG",
          "references" : [ ]
        }, {
          "name" : "INVALID_SESSION_ID",
          "references" : [ ]
        }, {
          "name" : "INVALID_SETUP_OWNER",
          "references" : [ ]
        }, {
          "name" : "INVALID_SIGNUP_COUNTRY",
          "references" : [ ]
        }, {
          "name" : "INVALID_STATUS",
          "references" : [ ]
        }, {
          "name" : "INVALID_TYPE",
          "references" : [ ]
        }, {
          "name" : "INVALID_TYPE_FOR_OPERATION",
          "references" : [ ]
        }, {
          "name" : "INVALID_TYPE_ON_FIELD_IN_RECORD",
          "references" : [ ]
        }, {
          "name" : "IP_RANGE_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "LICENSE_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "LIGHT_PORTAL_USER_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MALFORMED_ID",
          "references" : [ ]
        }, {
          "name" : "MANAGER_NOT_DEFINED",
          "references" : [ ]
        }, {
          "name" : "MASSMAIL_RETRY_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MASS_MAIL_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAXIMUM_CCEMAILS_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAXIMUM_DASHBOARD_COMPONENTS_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAXIMUM_HIERARCHY_LEVELS_REACHED",
          "references" : [ ]
        }, {
          "name" : "MAXIMUM_SIZE_OF_ATTACHMENT",
          "references" : [ ]
        }, {
          "name" : "MAXIMUM_SIZE_OF_DOCUMENT",
          "references" : [ ]
        }, {
          "name" : "MAX_ACTIONS_PER_RULE_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_ACTIVE_RULES_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_APPROVAL_STEPS_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_FORMULAS_PER_RULE_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_RULES_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_RULE_ENTRIES_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_TASK_DESCRIPTION_EXCEEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_TM_RULES_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MAX_TM_RULE_ITEMS_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "MERGE_FAILED",
          "references" : [ ]
        }, {
          "name" : "MISSING_ARGUMENT",
          "references" : [ ]
        }, {
          "name" : "MIXED_DML_OPERATION",
          "references" : [ ]
        }, {
          "name" : "NONUNIQUE_SHIPPING_ADDRESS",
          "references" : [ ]
        }, {
          "name" : "NO_APPLICABLE_PROCESS",
          "references" : [ ]
        }, {
          "name" : "NO_ATTACHMENT_PERMISSION",
          "references" : [ ]
        }, {
          "name" : "NO_INACTIVE_DIVISION_MEMBERS",
          "references" : [ ]
        }, {
          "name" : "NO_MASS_MAIL_PERMISSION",
          "references" : [ ]
        }, {
          "name" : "NO_SUCH_USER_EXISTS",
          "references" : [ ]
        }, {
          "name" : "NUMBER_OUTSIDE_VALID_RANGE",
          "references" : [ ]
        }, {
          "name" : "NUM_HISTORY_FIELDS_BY_SOBJECT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "OPTED_OUT_OF_MASS_MAIL",
          "references" : [ ]
        }, {
          "name" : "OP_WITH_INVALID_USER_TYPE_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "PACKAGE_LICENSE_REQUIRED",
          "references" : [ ]
        }, {
          "name" : "PACKAGING_API_INSTALL_FAILED",
          "references" : [ ]
        }, {
          "name" : "PACKAGING_API_UNINSTALL_FAILED",
          "references" : [ ]
        }, {
          "name" : "PORTAL_NO_ACCESS",
          "references" : [ ]
        }, {
          "name" : "PORTAL_USER_ALREADY_EXISTS_FOR_CONTACT",
          "references" : [ ]
        }, {
          "name" : "PRIVATE_CONTACT_ON_ASSET",
          "references" : [ ]
        }, {
          "name" : "QUERY_TIMEOUT",
          "references" : [ ]
        }, {
          "name" : "RECORD_IN_USE_BY_WORKFLOW",
          "references" : [ ]
        }, {
          "name" : "REQUEST_RUNNING_TOO_LONG",
          "references" : [ ]
        }, {
          "name" : "REQUIRED_FEATURE_MISSING",
          "references" : [ ]
        }, {
          "name" : "REQUIRED_FIELD_MISSING",
          "references" : [ ]
        }, {
          "name" : "SELF_REFERENCE_FROM_FLOW",
          "references" : [ ]
        }, {
          "name" : "SELF_REFERENCE_FROM_TRIGGER",
          "references" : [ ]
        }, {
          "name" : "SHARE_NEEDED_FOR_CHILD_OWNER",
          "references" : [ ]
        }, {
          "name" : "SINGLE_EMAIL_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "STANDARD_PRICE_NOT_DEFINED",
          "references" : [ ]
        }, {
          "name" : "STORAGE_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "STRING_TOO_LONG",
          "references" : [ ]
        }, {
          "name" : "TABSET_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "TEMPLATE_NOT_ACTIVE",
          "references" : [ ]
        }, {
          "name" : "TEMPLATE_NOT_FOUND",
          "references" : [ ]
        }, {
          "name" : "TERRITORY_REALIGN_IN_PROGRESS",
          "references" : [ ]
        }, {
          "name" : "TEXT_DATA_OUTSIDE_SUPPORTED_CHARSET",
          "references" : [ ]
        }, {
          "name" : "TOO_MANY_APEX_REQUESTS",
          "references" : [ ]
        }, {
          "name" : "TOO_MANY_ENUM_VALUE",
          "references" : [ ]
        }, {
          "name" : "TOO_MANY_POSSIBLE_USERS_EXIST",
          "references" : [ ]
        }, {
          "name" : "TRANSFER_REQUIRES_READ",
          "references" : [ ]
        }, {
          "name" : "UNABLE_TO_LOCK_ROW",
          "references" : [ ]
        }, {
          "name" : "UNAVAILABLE_RECORDTYPE_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "UNDELETE_FAILED",
          "references" : [ ]
        }, {
          "name" : "UNKNOWN_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "UNSPECIFIED_EMAIL_ADDRESS",
          "references" : [ ]
        }, {
          "name" : "UNSUPPORTED_APEX_TRIGGER_OPERATON",
          "references" : [ ]
        }, {
          "name" : "UNVERIFIED_SENDER_ADDRESS",
          "references" : [ ]
        }, {
          "name" : "USER_OWNS_PORTAL_ACCOUNT_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "USER_WITH_APEX_SHARES_EXCEPTION",
          "references" : [ ]
        }, {
          "name" : "WEBLINK_SIZE_LIMIT_EXCEEDED",
          "references" : [ ]
        }, {
          "name" : "WEBLINK_URL_INVALID",
          "references" : [ ]
        }, {
          "name" : "WRONG_CONTROLLER_TYPE",
          "references" : [ ]
        } ]
      },
      "String" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "maxWidth",
            "type" : "Integer"
          } ],
          "name" : "abbreviate",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "maxWidth",
            "type" : "Integer"
          }, {
            "name" : "offset",
            "type" : "Integer"
          } ],
          "name" : "abbreviate",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "capitalize",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "size",
            "type" : "Integer"
          } ],
          "name" : "center",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "String" ],
          "parameters" : [ {
            "name" : "size",
            "type" : "Integer"
          }, {
            "name" : "padStr",
            "type" : "String"
          } ],
          "name" : "center",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "compareTo",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "contains",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "validChars",
            "type" : "String"
          } ],
          "name" : "containsAny",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          } ],
          "name" : "containsIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "invalidChars",
            "type" : "String"
          } ],
          "name" : "containsNone",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "validChars",
            "type" : "String"
          } ],
          "name" : "containsOnly",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "containsWhitespace",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          } ],
          "name" : "countMatches",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "deleteWhitespace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          } ],
          "name" : "difference",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "endsWith",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "suffix",
            "type" : "String"
          } ],
          "name" : "endsWithIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          } ],
          "name" : "equalsIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "escapeCsv",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "escapeEcmaScript",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "escapeHtml3",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "escapeHtml4",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "s",
            "type" : "String"
          } ],
          "name" : "escapeSingleQuotes",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "escapeXml",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "LIST<String>" ],
          "parameters" : [ {
            "name" : "format",
            "type" : "String"
          }, {
            "name" : "arguments",
            "type" : "LIST<String>"
          } ],
          "name" : "format",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "LIST<Integer>" ],
          "parameters" : [ {
            "name" : "charArr",
            "type" : "LIST<Integer>"
          } ],
          "name" : "fromCharArray",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "LIST" ],
          "parameters" : [ {
            "name" : "strings",
            "type" : "LIST"
          } ],
          "name" : "getCommonPrefix",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          } ],
          "name" : "getLevenshteinDistance",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          }, {
            "name" : "threshold",
            "type" : "Integer"
          } ],
          "name" : "getLevenshteinDistance",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashCode",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "indexOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          }, {
            "name" : "startPos",
            "type" : "Integer"
          } ],
          "name" : "indexOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchChars",
            "type" : "String"
          } ],
          "name" : "indexOfAny",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchChars",
            "type" : "String"
          } ],
          "name" : "indexOfAnyBut",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "String"
          } ],
          "name" : "indexOfDifference",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          } ],
          "name" : "indexOfIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          }, {
            "name" : "startPos",
            "type" : "Integer"
          } ],
          "name" : "indexOfIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAllLowerCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAllUpperCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAlpha",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAlphaSpace",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAlphanumeric",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAlphanumericSpace",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isAsciiPrintable",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "isBlank",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "isEmpty",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "isNotBlank",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "isNotEmpty",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isNumeric",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isNumericSpace",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isWhitespace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "APEX_OBJECT", "String" ],
          "parameters" : [ {
            "name" : "iterableObj",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "separator",
            "type" : "String"
          } ],
          "name" : "join",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          }, {
            "name" : "startPos",
            "type" : "Integer"
          } ],
          "name" : "lastIndexOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "lastIndexOf",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          } ],
          "name" : "lastIndexOfIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "searchStr",
            "type" : "String"
          }, {
            "name" : "startPos",
            "type" : "Integer"
          } ],
          "name" : "lastIndexOfIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          } ],
          "name" : "left",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          } ],
          "name" : "leftPad",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "String" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          }, {
            "name" : "padStr",
            "type" : "String"
          } ],
          "name" : "leftPad",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "length",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "pos",
            "type" : "Integer"
          }, {
            "name" : "len",
            "type" : "Integer"
          } ],
          "name" : "mid",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "normalizeSpace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "overlay",
            "type" : "String"
          }, {
            "name" : "start",
            "type" : "Integer"
          }, {
            "name" : "end",
            "type" : "Integer"
          } ],
          "name" : "overlay",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "toRemove",
            "type" : "String"
          } ],
          "name" : "remove",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "toRemove",
            "type" : "String"
          } ],
          "name" : "removeEnd",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "toRemove",
            "type" : "String"
          } ],
          "name" : "removeEndIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "toRemove",
            "type" : "String"
          } ],
          "name" : "removeStart",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "toRemove",
            "type" : "String"
          } ],
          "name" : "removeStartIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "numTimes",
            "type" : "Integer"
          } ],
          "name" : "repeat",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "separator",
            "type" : "String"
          }, {
            "name" : "numTimes",
            "type" : "Integer"
          } ],
          "name" : "repeat",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "target",
            "type" : "String"
          }, {
            "name" : "replacement",
            "type" : "String"
          } ],
          "name" : "replace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          }, {
            "name" : "replacement",
            "type" : "String"
          } ],
          "name" : "replaceAll",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          }, {
            "name" : "replacement",
            "type" : "String"
          } ],
          "name" : "replaceFirst",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "reverse",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          } ],
          "name" : "right",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          } ],
          "name" : "rightPad",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "String" ],
          "parameters" : [ {
            "name" : "len",
            "type" : "Integer"
          }, {
            "name" : "padStr",
            "type" : "String"
          } ],
          "name" : "rightPad",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          } ],
          "name" : "split",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ "String", "Integer" ],
          "parameters" : [ {
            "name" : "regex",
            "type" : "String"
          }, {
            "name" : "limit",
            "type" : "Integer"
          } ],
          "name" : "split",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "splitByCharacterType",
          "references" : [ ]
        }, {
          "returnType" : "LIST<String>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "splitByCharacterTypeCamelCase",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "str",
            "type" : "String"
          } ],
          "name" : "startsWith",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          } ],
          "name" : "startsWithIgnoreCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "stripHtmlTags",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "start",
            "type" : "Integer"
          } ],
          "name" : "substring",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "start",
            "type" : "Integer"
          }, {
            "name" : "end",
            "type" : "Integer"
          } ],
          "name" : "substring",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "separator",
            "type" : "String"
          } ],
          "name" : "substringAfter",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "separator",
            "type" : "String"
          } ],
          "name" : "substringAfterLast",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "separator",
            "type" : "String"
          } ],
          "name" : "substringBefore",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "separator",
            "type" : "String"
          } ],
          "name" : "substringBeforeLast",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "open",
            "type" : "String"
          }, {
            "name" : "close",
            "type" : "String"
          } ],
          "name" : "substringBetween",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "tag",
            "type" : "String"
          } ],
          "name" : "substringBetween",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "swapCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toLowerCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "locale",
            "type" : "String"
          } ],
          "name" : "toLowerCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toUpperCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "locale",
            "type" : "String"
          } ],
          "name" : "toUpperCase",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "trim",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "uncapitalize",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "unescapeCsv",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "unescapeEcmaScript",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "unescapeHtml3",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "unescapeHtml4",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "unescapeXml",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Date"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Datetime" ],
          "parameters" : [ {
            "name" : "dt",
            "type" : "Datetime"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Decimal" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Decimal"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Double" ],
          "parameters" : [ {
            "name" : "d",
            "type" : "Double"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "i",
            "type" : "Integer"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Long" ],
          "parameters" : [ {
            "name" : "l",
            "type" : "Long"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "valueOf",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Datetime" ],
          "parameters" : [ {
            "name" : "dt",
            "type" : "Datetime"
          } ],
          "name" : "valueOfGmt",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "StringException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "System" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "jobId",
            "type" : "String"
          } ],
          "name" : "abortJob",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "condition",
            "type" : "Boolean"
          } ],
          "name" : "assert",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean", "ANY" ],
          "parameters" : [ {
            "name" : "condition",
            "type" : "Boolean"
          }, {
            "name" : "msg",
            "type" : "ANY"
          } ],
          "name" : "assert",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY", "ANY" ],
          "parameters" : [ {
            "name" : "expected",
            "type" : "ANY"
          }, {
            "name" : "actual",
            "type" : "ANY"
          } ],
          "name" : "assertEquals",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY", "ANY", "ANY" ],
          "parameters" : [ {
            "name" : "expected",
            "type" : "ANY"
          }, {
            "name" : "actual",
            "type" : "ANY"
          }, {
            "name" : "msg",
            "type" : "ANY"
          } ],
          "name" : "assertEquals",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY", "ANY" ],
          "parameters" : [ {
            "name" : "expected",
            "type" : "ANY"
          }, {
            "name" : "actual",
            "type" : "ANY"
          } ],
          "name" : "assertNotEquals",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY", "ANY", "ANY" ],
          "parameters" : [ {
            "name" : "expected",
            "type" : "ANY"
          }, {
            "name" : "actual",
            "type" : "ANY"
          }, {
            "name" : "msg",
            "type" : "ANY"
          } ],
          "name" : "assertNotEquals",
          "references" : [ ]
        }, {
          "returnType" : "System.PageReference",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "currentPageReference",
          "references" : [ ]
        }, {
          "returnType" : "Long",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "currentTimeMillis",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "ANY"
          } ],
          "name" : "debug",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "ANY" ],
          "parameters" : [ {
            "name" : "logLevel",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "o",
            "type" : "ANY"
          } ],
          "name" : "debug",
          "references" : [ ]
        }, {
          "returnType" : "system.ApplicationReadWriteMode",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getApplicationReadWriteMode",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isBatch",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isFuture",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isScheduled",
          "references" : [ ]
        }, {
          "returnType" : "Datetime",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "now",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "LIST", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "workitemIds",
            "type" : "LIST"
          }, {
            "name" : "action",
            "type" : "String"
          }, {
            "name" : "commments",
            "type" : "String"
          }, {
            "name" : "nextApprover",
            "type" : "String"
          } ],
          "name" : "process",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Date" ],
          "parameters" : [ {
            "name" : "date",
            "type" : "Date"
          } ],
          "name" : "purgeOldAsyncJobs",
          "references" : [ ]
        }, {
          "returnType" : "system.Version",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "requestVersion",
          "references" : [ ]
        }, {
          "returnType" : "System.ResetPasswordResult",
          "argTypes" : [ "Id", "Boolean" ],
          "parameters" : [ {
            "name" : "userId",
            "type" : "Id"
          }, {
            "name" : "sendUserEmail",
            "type" : "Boolean"
          } ],
          "name" : "resetPassword",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Package.Version" ],
          "parameters" : [ {
            "name" : "version",
            "type" : "Package.Version"
          } ],
          "name" : "runAs",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "SObject", "ANY" ],
          "parameters" : [ {
            "name" : "user",
            "type" : "SObject"
          }, {
            "name" : "block",
            "type" : "ANY"
          } ],
          "name" : "runAs",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String", "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "jobName",
            "type" : "String"
          }, {
            "name" : "cronExp",
            "type" : "String"
          }, {
            "name" : "schedulable",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "schedule",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "APEX_OBJECT", "String", "Integer" ],
          "parameters" : [ {
            "name" : "batchable",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "jobName",
            "type" : "String"
          }, {
            "name" : "minutesFromNow",
            "type" : "Integer"
          } ],
          "name" : "scheduleBatch",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "APEX_OBJECT", "String", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "batchable",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "jobName",
            "type" : "String"
          }, {
            "name" : "minutesFromNow",
            "type" : "Integer"
          }, {
            "name" : "scopeSize",
            "type" : "Integer"
          } ],
          "name" : "scheduleBatch",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Id", "String" ],
          "parameters" : [ {
            "name" : "userId",
            "type" : "Id"
          }, {
            "name" : "password",
            "type" : "String"
          } ],
          "name" : "setPassword",
          "references" : [ ]
        }, {
          "returnType" : "LIST<Id>",
          "argTypes" : [ "LIST", "String", "String" ],
          "parameters" : [ {
            "name" : "ids",
            "type" : "LIST"
          }, {
            "name" : "commments",
            "type" : "String"
          }, {
            "name" : "nextApprover",
            "type" : "String"
          } ],
          "name" : "submit",
          "references" : [ ]
        }, {
          "returnType" : "Date",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "today",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Test" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "Test",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Component.apex.page",
          "argTypes" : [ "System.PageReference" ],
          "parameters" : [ {
            "name" : "p",
            "type" : "System.PageReference"
          } ],
          "name" : "invokePage",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isRunningTest",
          "references" : [ ]
        }, {
          "returnType" : "LIST<SObject>",
          "argTypes" : [ "Schema.SObjectType", "String" ],
          "parameters" : [ {
            "name" : "sobjectType",
            "type" : "Schema.SObjectType"
          }, {
            "name" : "staticResourceName",
            "type" : "String"
          } ],
          "name" : "loadData",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "pageReference",
            "type" : "Object"
          } ],
          "name" : "setCurrentPage",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "pageReference",
            "type" : "Object"
          } ],
          "name" : "setCurrentPageReference",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "LIST<String>" ],
          "parameters" : [ {
            "name" : "searchResultsIds",
            "type" : "LIST<String>"
          } ],
          "name" : "setFixedSearchResults",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "system.Type", "Object" ],
          "parameters" : [ {
            "name" : "interfaceType",
            "type" : "system.Type"
          }, {
            "name" : "mock",
            "type" : "Object"
          } ],
          "name" : "setMock",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "readOnlyApplicationMode",
            "type" : "Boolean"
          } ],
          "name" : "setReadOnlyApplicationMode",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "startTest",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "stopTest",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "system.InstallHandler", "system.Version" ],
          "parameters" : [ {
            "name" : "script",
            "type" : "system.InstallHandler"
          }, {
            "name" : "version",
            "type" : "system.Version"
          } ],
          "name" : "testInstall",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "system.InstallHandler", "system.Version", "Boolean" ],
          "parameters" : [ {
            "name" : "script",
            "type" : "system.InstallHandler"
          }, {
            "name" : "version",
            "type" : "system.Version"
          }, {
            "name" : "isPush",
            "type" : "Boolean"
          } ],
          "name" : "testInstall",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "system.UninstallHandler" ],
          "parameters" : [ {
            "name" : "script",
            "type" : "system.UninstallHandler"
          } ],
          "name" : "testUninstall",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Time" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "APEX_OBJECT"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "Boolean" ],
          "parameters" : [ {
            "name" : "msg",
            "type" : "String"
          }, {
            "name" : "escape",
            "type" : "Boolean"
          } ],
          "name" : "addError",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "hours",
            "type" : "Integer"
          } ],
          "name" : "addHours",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "milliseconds",
            "type" : "Integer"
          } ],
          "name" : "addMilliseconds",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "minutes",
            "type" : "Integer"
          } ],
          "name" : "addMinutes",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "seconds",
            "type" : "Integer"
          } ],
          "name" : "addSeconds",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hour",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "millisecond",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "minute",
          "references" : [ ]
        }, {
          "returnType" : "Time",
          "argTypes" : [ "Integer", "Integer", "Integer", "Integer" ],
          "parameters" : [ {
            "name" : "hour",
            "type" : "Integer"
          }, {
            "name" : "minute",
            "type" : "Integer"
          }, {
            "name" : "second",
            "type" : "Integer"
          }, {
            "name" : "millisecond",
            "type" : "Integer"
          } ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "second",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "TimeZone" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDisplayName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getID",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ "Datetime" ],
          "parameters" : [ {
            "name" : "dt",
            "type" : "Datetime"
          } ],
          "name" : "getOffset",
          "references" : [ ]
        }, {
          "returnType" : "system.TimeZone",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "id",
            "type" : "String"
          } ],
          "name" : "getTimeZone",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "TouchHandledException" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          } ],
          "name" : null,
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Type" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Boolean",
          "argTypes" : [ "Object" ],
          "parameters" : [ {
            "name" : "o",
            "type" : "Object"
          } ],
          "name" : "equals",
          "references" : [ ]
        }, {
          "returnType" : "system.Type",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "clsName",
            "type" : "String"
          } ],
          "name" : "forName",
          "references" : [ ]
        }, {
          "returnType" : "system.Type",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "namespace",
            "type" : "String"
          }, {
            "name" : "clsName",
            "type" : "String"
          } ],
          "name" : "forName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getName",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hashcode",
          "references" : [ ]
        }, {
          "returnType" : "Object",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "newInstance",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "TypeException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "UnexpectedException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "UnsupportedOperationException" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UnsupportedOperationException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "Exception"
          } ],
          "name" : "UnsupportedOperationException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          } ],
          "name" : "UnsupportedOperationException",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "param1",
            "type" : "String"
          }, {
            "name" : "param2",
            "type" : "Exception"
          } ],
          "name" : "UnsupportedOperationException",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Url" : {
        "constructors" : [ {
          "parameters" : [ {
            "name" : "protocol",
            "type" : "String"
          }, {
            "name" : "host",
            "type" : "String"
          }, {
            "name" : "port",
            "type" : "Integer"
          }, {
            "name" : "file",
            "type" : "String"
          } ],
          "name" : "Url",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "protocol",
            "type" : "String"
          }, {
            "name" : "host",
            "type" : "String"
          }, {
            "name" : "file",
            "type" : "String"
          } ],
          "name" : "Url",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "spec",
            "type" : "String"
          } ],
          "name" : "Url",
          "references" : [ ]
        }, {
          "parameters" : [ {
            "name" : "context",
            "type" : "system.Url"
          }, {
            "name" : "spec",
            "type" : "String"
          } ],
          "name" : "Url",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAuthority",
          "references" : [ ]
        }, {
          "returnType" : "system.Url",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCurrentRequestUrl",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDefaultPort",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getFile",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "objectId",
            "type" : "String"
          }, {
            "name" : "fieldName",
            "type" : "String"
          } ],
          "name" : "getFileFieldURL",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getHost",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPath",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPort",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getProtocol",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getQuery",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRef",
          "references" : [ ]
        }, {
          "returnType" : "system.Url",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSalesforceBaseUrl",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserInfo",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "system.Url" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "system.Url"
          } ],
          "name" : "sameFile",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toExternalForm",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "UserInfo" : {
        "constructors" : [ {
          "parameters" : [ ],
          "name" : "UserInfo",
          "references" : [ ]
        } ],
        "methods" : [ {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getDefaultCurrency",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getFirstName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLanguage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLastName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLocale",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getOrganizationId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getOrganizationName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getProfileId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getSessionId",
          "references" : [ ]
        }, {
          "returnType" : "system.TimeZone",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTimeZone",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUiTheme",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUiThemeDisplayed",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserEmail",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserRoleId",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getUserType",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "namespacePrefix",
            "type" : "String"
          } ],
          "name" : "isCurrentUserLicensed",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isMultiCurrencyOrganization",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "Version" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Integer",
          "argTypes" : [ "system.Version" ],
          "parameters" : [ {
            "name" : "other",
            "type" : "system.Version"
          } ],
          "name" : "compareTo",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "major",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "minor",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "patch",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "VisualforceException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "WebServiceMock" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ "Object", "Object", "MAP<String,ANY>", "String", "String", "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "param1",
            "type" : "Object"
          }, {
            "name" : "param2",
            "type" : "Object"
          }, {
            "name" : "param3",
            "type" : "MAP<String,ANY>"
          }, {
            "name" : "param4",
            "type" : "String"
          }, {
            "name" : "param5",
            "type" : "String"
          }, {
            "name" : "param6",
            "type" : "String"
          }, {
            "name" : "param7",
            "type" : "String"
          }, {
            "name" : "param8",
            "type" : "String"
          }, {
            "name" : "param9",
            "type" : "String"
          } ],
          "name" : "doInvoke",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlException" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Exception",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getCause",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLineNumber",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getMessage",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getStackTraceString",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getTypeName",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "APEX_OBJECT" ],
          "parameters" : [ {
            "name" : "cause",
            "type" : "APEX_OBJECT"
          } ],
          "name" : "initCause",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "message",
            "type" : "String"
          } ],
          "name" : "setMessage",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlStreamReader" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAttributeCount",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeLocalName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeNamespace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributePrefix",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeType",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "namespaceURI",
            "type" : "String"
          }, {
            "name" : "localName",
            "type" : "String"
          } ],
          "name" : "getAttributeValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeValueAt",
          "references" : [ ]
        }, {
          "returnType" : "system.XmlTag",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getEventType",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLocalName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getLocation",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNamespace",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNamespaceCount",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getNamespacePrefix",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          } ],
          "name" : "getNamespaceURI",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getNamespaceURIAt",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPIData",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPITarget",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getPrefix",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getText",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getVersion",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasName",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasNext",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "hasText",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isCharacters",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isEndElement",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isStartElement",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "isWhitespace",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "next",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "nextTag",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "flag",
            "type" : "Boolean"
          } ],
          "name" : "setCoalescing",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "Boolean" ],
          "parameters" : [ {
            "name" : "flag",
            "type" : "Boolean"
          } ],
          "name" : "setNamespaceAware",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlStreamWriter" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "close",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getXmlString",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "uri",
            "type" : "String"
          } ],
          "name" : "setDefaultNamespace",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          }, {
            "name" : "namespaceURI",
            "type" : "String"
          }, {
            "name" : "localName",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "writeAttribute",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "data",
            "type" : "String"
          } ],
          "name" : "writeCData",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "text",
            "type" : "String"
          } ],
          "name" : "writeCharacters",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "data",
            "type" : "String"
          } ],
          "name" : "writeComment",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "namesapceURI",
            "type" : "String"
          } ],
          "name" : "writeDefaultNamespace",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          }, {
            "name" : "localName",
            "type" : "String"
          }, {
            "name" : "namesapceURI",
            "type" : "String"
          } ],
          "name" : "writeEmptyElement",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeEndDocument",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "writeEndElement",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          }, {
            "name" : "namesapceURI",
            "type" : "String"
          } ],
          "name" : "writeNamespace",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "target",
            "type" : "String"
          }, {
            "name" : "data",
            "type" : "String"
          } ],
          "name" : "writeProcessingInstruction",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "encoding",
            "type" : "String"
          }, {
            "name" : "version",
            "type" : "String"
          } ],
          "name" : "writeStartDocument",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          }, {
            "name" : "localName",
            "type" : "String"
          }, {
            "name" : "namesapceURI",
            "type" : "String"
          } ],
          "name" : "writeStartElement",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlTag" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<system.XmlTag>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "ATTRIBUTE",
          "references" : [ ]
        }, {
          "name" : "CDATA",
          "references" : [ ]
        }, {
          "name" : "CHARACTERS",
          "references" : [ ]
        }, {
          "name" : "COMMENT",
          "references" : [ ]
        }, {
          "name" : "DTD",
          "references" : [ ]
        }, {
          "name" : "END_DOCUMENT",
          "references" : [ ]
        }, {
          "name" : "END_ELEMENT",
          "references" : [ ]
        }, {
          "name" : "ENTITY_DECLARATION",
          "references" : [ ]
        }, {
          "name" : "ENTITY_REFERENCE",
          "references" : [ ]
        }, {
          "name" : "NAMESPACE",
          "references" : [ ]
        }, {
          "name" : "NOTATION_DECLARATION",
          "references" : [ ]
        }, {
          "name" : "PROCESSING_INSTRUCTION",
          "references" : [ ]
        }, {
          "name" : "SPACE",
          "references" : [ ]
        }, {
          "name" : "START_DOCUMENT",
          "references" : [ ]
        }, {
          "name" : "START_ELEMENT",
          "references" : [ ]
        } ]
      }
    },
    "dom" : {
      "Document" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "namespace",
            "type" : "String"
          }, {
            "name" : "prefix",
            "type" : "String"
          } ],
          "name" : "createRootElement",
          "references" : [ ]
        }, {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getRootElement",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "xml",
            "type" : "String"
          } ],
          "name" : "load",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "toXmlString",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlNode" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ "String", "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "namespace",
            "type" : "String"
          }, {
            "name" : "prefix",
            "type" : "String"
          } ],
          "name" : "addChildElement",
          "references" : [ ]
        }, {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "text",
            "type" : "String"
          } ],
          "name" : "addCommentNode",
          "references" : [ ]
        }, {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "text",
            "type" : "String"
          } ],
          "name" : "addTextNode",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "keyNamespace",
            "type" : "String"
          } ],
          "name" : "getAttribute",
          "references" : [ ]
        }, {
          "returnType" : "Integer",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getAttributeCount",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeKeyAt",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "Integer" ],
          "parameters" : [ {
            "name" : "index",
            "type" : "Integer"
          } ],
          "name" : "getAttributeKeyNsAt",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "keyNamespace",
            "type" : "String"
          } ],
          "name" : "getAttributeValue",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "keyNamespace",
            "type" : "String"
          } ],
          "name" : "getAttributeValueNs",
          "references" : [ ]
        }, {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "name",
            "type" : "String"
          }, {
            "name" : "namespace",
            "type" : "String"
          } ],
          "name" : "getChildElement",
          "references" : [ ]
        }, {
          "returnType" : "LIST<dom.XmlNode>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getChildElements",
          "references" : [ ]
        }, {
          "returnType" : "LIST<dom.XmlNode>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getChildren",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getName",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNamespace",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          } ],
          "name" : "getNamespaceFor",
          "references" : [ ]
        }, {
          "returnType" : "Dom.XmlNodeType",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getNodeType",
          "references" : [ ]
        }, {
          "returnType" : "dom.XmlNode",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getParent",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ "String" ],
          "parameters" : [ {
            "name" : "namespace",
            "type" : "String"
          } ],
          "name" : "getPrefixFor",
          "references" : [ ]
        }, {
          "returnType" : "String",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "getText",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "keyNamespace",
            "type" : "String"
          } ],
          "name" : "removeAttribute",
          "references" : [ ]
        }, {
          "returnType" : "Boolean",
          "argTypes" : [ "ANY" ],
          "parameters" : [ {
            "name" : "child",
            "type" : "ANY"
          } ],
          "name" : "removeChild",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          } ],
          "name" : "setAttribute",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String", "String", "String" ],
          "parameters" : [ {
            "name" : "key",
            "type" : "String"
          }, {
            "name" : "value",
            "type" : "String"
          }, {
            "name" : "keyNamespace",
            "type" : "String"
          }, {
            "name" : "valueNamespace",
            "type" : "String"
          } ],
          "name" : "setAttributeNs",
          "references" : [ ]
        }, {
          "returnType" : "void",
          "argTypes" : [ "String", "String" ],
          "parameters" : [ {
            "name" : "prefix",
            "type" : "String"
          }, {
            "name" : "namespace",
            "type" : "String"
          } ],
          "name" : "setNamespace",
          "references" : [ ]
        } ],
        "properties" : [ ]
      },
      "XmlNodeType" : {
        "constructors" : [ ],
        "methods" : [ {
          "returnType" : "LIST<Dom.XmlNodeType>",
          "argTypes" : [ ],
          "parameters" : [ ],
          "name" : "values",
          "references" : [ ]
        } ],
        "properties" : [ {
          "name" : "COMMENT",
          "references" : [ ]
        }, {
          "name" : "ELEMENT",
          "references" : [ ]
        }, {
          "name" : "TEXT",
          "references" : [ ]
        } ]
      }
    }
  }
}