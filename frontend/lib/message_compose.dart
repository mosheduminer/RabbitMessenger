import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:rich_input/rich_input.dart';

typedef Callback = void Function(String);

class SendIntent extends Intent {}

class MessageComposer extends StatelessWidget {
  MessageComposer(this.sendCallback);

  final Callback sendCallback;
  final _controller = RichInputController();

  void _send() {
    sendCallback(_controller.data);
    _controller.clear();
  }

  Widget shortcuts({required child}) {
    return Shortcuts(
      shortcuts: {
        LogicalKeySet(LogicalKeyboardKey.control, LogicalKeyboardKey.enter):
            SendIntent(),
      },
      child: Actions(actions: {
        SendIntent: CallbackAction<SendIntent>(
            onInvoke: (SendIntent intent) => _send()),
      }, child: child),
    );
  }

  @override
  Widget build(BuildContext context) {
    return shortcuts(
        child: Container(
      padding: EdgeInsets.only(right: 10, left: 10, bottom: 10, top: 4),
      child: Container(
        decoration: BoxDecoration(boxShadow: [
          BoxShadow(color: Colors.grey, blurRadius: 5, spreadRadius: 5)
        ], borderRadius: BorderRadius.all(Radius.circular(10))),
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                    color: Colors.white70,
                    borderRadius: BorderRadius.all(Radius.circular(5))),
                padding: EdgeInsets.symmetric(horizontal: 15),
                child: RichInput(
                    decoration: InputDecoration(border: InputBorder.none),
                    minLines: 1,
                    maxLines: 5,
                    controller: _controller),
              ),
            ),
            IconButton(
                color: Colors.blue[800],
                icon: Icon(Icons.send),
                tooltip: 'Send',
                onPressed: _send)
          ],
        ),
      ),
    ));
  }
}
