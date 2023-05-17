# 🔐 FT_OTP: One-Time Password Generator 🕑

FT_OTP is a robust and reliable tool that allows you to manage an initial key and generate a new one-time password (OTP) whenever you need one. 
It's like having a secure vault in your toolbox! 🔒

## 🚀 Usage

To use FT_OTP, just call the program with the desired option:

```bash
./ft_otp [-gk] 
```

🛠️ Options

FT_OTP provides the following options to manage and generate your OTPs:

    -g : With this option, the program accepts a hexadecimal key of at least 64 characters as an argument. 
    FT_OTP will securely store this key in a file called ft_otp.key, which will always be encrypted. 🔑

bash

./ft_otp -g [hexadecimal_key]

    -k : This option will trigger FT_OTP to generate a new temporary password and display it on the standard output. 
    Your new OTP is just a command away! 🎲

bash

./ft_otp -k

**🕵️‍♂️ Security**

We take security seriously. The key is stored in an encrypted form and the OTPs are generated in a secure manner. 
However, remember to keep your initial key and generated OTPs safe. 🔐

**🎉 Start Generating OTPs!**

Now that you know how to use FT_OTP, start generating OTPs for your needs! Remember, security is paramount, 
so always use strong keys and manage your OTPs responsibly.

**📝 License**

This project is licensed under the MIT License. Feel free to use and modify the code as you like!
