# Find temperture and pH of related organism by EC number

This is a small script to retrieve information about the temperature and pH value of various organisms with the same EC number for an enzyme, based on the [Brenda database][1]. This is the [web app][3] version 

## Usage
For download the script:
```
git clone https://github.com/Truongphi20/ec2phtem
```
First, you must have a Brenda account, otherwise, you must register an account on Brenda's website. For running the script, you have just command:

```
python .\ec2phtem.py
```
And fill in your email, the password of Brenda's account, and finally is EC number of the desired enzyme 

Example result:

![image](https://user-images.githubusercontent.com/96680644/222891908-425be4a9-d3ae-4361-b59a-27fe3db7b412.png)

## Meaning of the columns

The reputation column is the number of citations of related articles. The meaning of other columns can be looked up on the guideline [SOAP website][2] of Brenda.


[1]: https://www.brenda-enzymes.org/
[2]: https://www.brenda-enzymes.org/soap.php
[3]: https://truongphi20-ec2phtem-main-streamlit-0vs5qq.streamlit.app/
