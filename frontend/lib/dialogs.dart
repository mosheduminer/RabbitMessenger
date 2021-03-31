import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

typedef SubmitCallback = void Function();

class BaseDialog extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    throw UnimplementedError();
  }

  Widget dialog(GlobalKey<FormState> formKey, Widget field,
      SubmitCallback submitCallback, String buttonText) {
    return AlertDialog(
      content: Form(
          key: formKey,
          child: Row(
            children: [
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: SizedBox(width: 350, child: field),
                  ),
                  ElevatedButton(
                      onPressed: submitCallback, child: Text(buttonText))
                ],
              ),
            ],
          )),
    );
  }
}

class AddContactDialog extends BaseDialog {
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return dialog(_formKey, inputField(), () => submitCallback(context),
        'Add User to Contacts');
  }

  Widget inputField() {
    return TextFormField(
        decoration: InputDecoration(labelText: 'Handle of New Contact'),
        controller: _controller,
        validator: (text) {
          if (text == null) {
            return 'Text is NULL, this is probably a bug';
          }
          if (text.length == 0) {
            return 'You must provide the handle of the contact you wish to add';
          }
          if (!text.contains('#')) {
            return 'You must provide a handle including the "#" followed by the number hash';
          }
          return null;
        });
  }

  void submitCallback(BuildContext context) {
    if (_formKey.currentState!.validate()) {
      print(_controller.text);
      Navigator.of(context).pop();
    }
  }
}

class CreateGroupDialog extends BaseDialog {
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return dialog(_formKey, inputField(), () => submitCallback(context),
        'Create new Group');
  }

  Widget inputField() {
    return TextFormField(
        decoration: InputDecoration(labelText: 'Name of New Group'),
        controller: _controller,
        validator: (text) {
          if (text == null) {
            return 'text is null. this is a bug';
          }
          if (text.length == 0) {
            return 'You must provide a name!';
          }
          return null;
        });
  }

  void submitCallback(BuildContext context) {
    if (_formKey.currentState!.validate()) {
      print(_controller.text);
      Navigator.of(context).pop();
    }
  }
}
