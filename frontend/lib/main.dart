import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sportbook/landing.dart';
import 'login_service.dart';
import 'default_service.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider<LoginService>(create: (context) => LoginService(),),
        ChangeNotifierProvider<DefaultService>(create: (context) => DefaultService(),)
      ],
      child: MyApp(),
    )
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Log",
      home: LandingPage()
    );
  }
}