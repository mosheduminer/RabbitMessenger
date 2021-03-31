import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import './dialogs.dart';
import './users.dart';

typedef EmptyReturnCallback = void Function(String, String);

class ChannelList extends StatefulWidget {
  ChannelList(this.callback);

  final EmptyReturnCallback callback;

  @override
  _ChannelListState createState() => _ChannelListState();
}

class _ChannelListState extends State<ChannelList> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: actions(),
        elevation: 1,
        backgroundColor: Colors.black54,
        title: Text('Chats',
            style:
                TextStyle(color: Colors.red[100], fontWeight: FontWeight.bold)),
      ),
      body: channels(50),
    );
  }

  List<Widget> actions() {
    return [
      IconButton(
          hoverColor: Colors.white54,
          tooltip: 'Create Group Chat',
          icon: Icon(
            Icons.group_add,
          ),
          onPressed: () {
            showDialog(
                context: context,
                builder: (context) {
                  return CreateGroupDialog();
                });
          }),
      IconButton(
          hoverColor: Colors.white54,
          tooltip: 'Add Contact',
          icon: Icon(Icons.person_add),
          onPressed: () {
            showDialog(
                context: context,
                builder: (context) {
                  return AddContactDialog();
                });
          }),
    ];
  }

  Widget channels(int amount) {
    return Users(amount, widget.callback);
  }
}
