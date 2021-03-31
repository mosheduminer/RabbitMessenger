import 'package:flutter/material.dart';
import 'channels.dart';

import 'chat.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Rabbit Messenger',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Rabbit Messenger'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Contact? currentChat;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;

    return Scaffold(
        body: Container(
      child: Row(
        children: [
          Container(
            constraints: BoxConstraints(maxWidth: width / 4),
            child: ChannelList((name, hash) {
              setState(() {
                currentChat = Contact(name, hash);
              });
            }),
          ),
          Container(
              constraints: BoxConstraints(maxWidth: width / 4 * 3),
              child: currentChat == null
                  ? Center(
                      child: Column(
                        children: [Text('Select a chat from the sidebar')],
                        mainAxisAlignment: MainAxisAlignment.center,
                      ),
                    )
                  : Chat(
                      name: currentChat!.name,
                      hash: currentChat!.hash,
                      closeCallback: () {
                        setState(() {
                          currentChat = null;
                        });
                      })),
        ],
      ),
    ));
  }
}

class Contact {
  Contact(this.name, this.hash);

  final String name;
  final String hash;
}
