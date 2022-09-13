login = {
  "title": "Sign in",
  "secondary": "Hello there, welcome back!",
  "method": "POST",
  "redirect_authenticated_user" : True,
}

pwdChangeForm = {
  "title": "Change Password",
  "secondary": "Apes together strong!",
  "method": "POST",
  "redirect_authenticated_user" : False,
}

pwdChangeDone = {
  "title": "Change Password Done",
  "context": "You have successfully changed your password!",
  "redirect_authenticated_user" : True,
}

pwdResetForm = {
  "title": "Reset Password",
  "secondary": "Password reset link will be sent to your email.",
  "method": "POST",
  "redirect_authenticated_user" : True,
}

pwdResetDone = {
  "title": "Reset link sent",
  "context": "A password reset link has been sent to your email address. Please check you Inbox and Spam folders.",
  "redirect_authenticated_user" : True,
}

pwdResetConfirm = {
  "title": "Reset Password",
  "secondary": "Enter a new password",
  "method": "POST",
  "redirect_authenticated_user" : True,
}

pwdResetComplete = {
  "title": "Password reset successful",
  "context": "You have successfully reset your password",
  "redirect_authenticated_user" : True,
}