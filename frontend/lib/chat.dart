import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:rabbit_messenger_frontend/message_compose.dart';

enum MessageDirection {
  sender,
  receiver,
}

class Dummy {
  final MessageDirection messageDirection;
  final String message;
  final DateTime dateTime;

  Dummy(this.message, this.messageDirection, this.dateTime);

  Dummy.get(int num)
      : dateTime = DateTime.now(),
        message = num.isEven
            ? 'Message Sender -  very long message so long. Let\'s not even talk about how long it really is'
            : 'Message Receiver',
        messageDirection =
            num.isEven ? MessageDirection.sender : MessageDirection.receiver;
}

class Chat extends StatelessWidget {
  final String name;
  final String hash;
  final VoidCallback closeCallback;

  Chat({required this.name, required this.hash, required this.closeCallback});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(icon: Icon(Icons.close), onPressed: closeCallback)
        ],
        elevation: 1,
        backgroundColor: Colors.white38,
        title: RichText(
            text: TextSpan(
                style: TextStyle(fontWeight: FontWeight.bold),
                children: [
              TextSpan(
                  text: name,
                  style: TextStyle(fontSize: 19, color: Colors.blue)),
              TextSpan(
                  text: '#',
                  style: TextStyle(
                      fontSize: 15,
                      color: Colors.grey[800],
                      fontStyle: FontStyle.italic)),
              TextSpan(
                  text: hash,
                  style: TextStyle(
                      fontSize: 15,
                      color: Colors.blueGrey[900],
                      fontStyle: FontStyle.italic))
            ])),
      ),
      body: messages(),
      bottomNavigationBar: MessageComposer((val) {
        print(val);
      }),
    );
  }

  Widget messages() {
    return ListView.builder(
        shrinkWrap: true,
        reverse: true,
        itemCount: 40,
        itemBuilder: (context, num) {
          return message(Dummy.get(num));
        });
  }

  Widget message(Dummy dummy) {
    Color color;
    Alignment alignment;
    Radius topRight;
    Radius topLeft;
    if (dummy.messageDirection == MessageDirection.sender) {
      color = Colors.blue[300]!;
      alignment = Alignment.bottomRight;
      topLeft = Radius.circular(20);
      topRight = Radius.zero;
    } else {
      color = Colors.grey[200]!;
      alignment = Alignment.bottomLeft;
      topLeft = Radius.zero;
      topRight = Radius.circular(20);
    }
    return Container(
        padding: EdgeInsets.symmetric(horizontal: 14, vertical: 5),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // display message, max-width of 0.45 of row
            // (which is equal to the width the messages area)
            Container(
              alignment: alignment,
              child: FractionallySizedBox(
                widthFactor: 0.45,
                child: Row(
                  children: [
                    Flexible(
                      child: Container(
                        padding: EdgeInsets.all(12),
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.only(
                              topLeft: topLeft,
                              topRight: topRight,
                              bottomLeft: Radius.circular(20),
                              bottomRight: Radius.circular(20),
                            ),
                            color: color),
                        child: SelectableText(dummy.message),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            // display datetime
            Align(
              alignment: alignment,
              child: Text(dummy.dateTime.toLocal().toString().split('.')[0],
                  style: TextStyle(fontSize: 12)),
            )
          ],
        ));
  }
}
