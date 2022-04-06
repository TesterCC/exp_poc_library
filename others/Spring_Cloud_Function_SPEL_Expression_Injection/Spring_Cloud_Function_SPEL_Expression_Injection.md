# Spring Cloud Function SPEL Expression Injection

Spring Cloud Function SPEL表达式注入漏洞


## Intro

Spring框架为现代基于java的企业应用程序(在任何类型的部署平台上)提供了一个全面的编程和配置模型。

Spring Cloud 中的 serveless框架 Spring Cloud Function 中的 RoutingFunction 类的 apply 方法将请求头中的“spring.cloud.function.routing-expression”参数作为 Spel 表达式进行处理，造成Spel表达式注入，攻击者可通过该漏洞执行任意代码。

## Condition

3.0.0.RELEASE <= Spring Cloud Function <= 3.2.2

## REF
- [Spring Cloud Function SPEL表达式注入漏洞](https://www.anquanke.com/post/id/271221)
- [SpringCloud Function SpEL漏洞环境搭建+漏洞复现](https://www.anquanke.com/post/id/271167)

## Analysis

调试笔记 [Spring-Cloud-Function-SPEL-debug-demo](https://github.com/TesterCC/Spring-Cloud-Function-SPEL-debug-demo)

