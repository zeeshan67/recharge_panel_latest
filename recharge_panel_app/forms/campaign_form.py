__author__ = 'ashish'

from django import forms


class CreateCampaignForm(forms.Form):
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','title': 'Mobile Number'}),min_length=10,
                                    max_length=12,
                                    required=True)

    recharge_type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Campaign Type'}), required=True)

    circle = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Circle'}), required=True)

    operator = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Operator'}), required=True)

    amount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control','title': 'Amount'}))

    file_switch = forms.BooleanField(widget=forms.HiddenInput(attrs={'value': "false"}), required=False)

    def __init__(self, *args, **kwargs):
        # user_id = kwargs.pop('user_id')
        super(CreateCampaignForm, self).__init__(*args, **kwargs)

        self.fields['recharge_type'].choices = ((("prepaid"), ("Prepaid")), (("postpaid"), ("Postpaid")))
        self.fields['circle'].choices = (((""), ("Select")),
                                        (("mumbai"), ("Mumbai")),
                                        (("maharashtra"), ("Maharashtra")),
                                        (("gujarat"),("Gujarat")),
                                        (("rajasthan"),("Rajasthan")),
                                        (("delhi"),("Delhi")),
                                        (("chennai"),("Chennai")),
                                        (("bihar"),("Bihar")),
                                        (("assam"),("Assam")),
                                        (("andhra_pradesh"),("Andhra Pradesh")),
                                        (("orissa"),("Orissa")),
                                        (("tamil_nadu"),("Tamil Nadu")),
                                        (("karnataka"), ("Karnataka")),
                                        (("kerala"), ("Kerala")),
                                        (("madhya_pradesh"),("Madhya Pradesh")),
                                        (("haryana"),("Haryana")),
                                        (("himachal_pradesh"),("Himachal Pradesh")),
                                        (("kolkata"),("Kolkata")),
                                        (("uttar_pradesh_east"),("Uttar Pradesh East")),
                                        (("uttar_pradesh_west"),("Uttar Pradesh West")),
                                        (("punjab"),("Punjab")),
                                        (("northeast"),("North-East")),
                                        (("jammu_kashmir"),("Jammu & Kashmir")),
        )
        self.fields['operator'].choices = (((""), ("Select")),(("airtel"), ("Airtel")), (("aircel"), ("Aircel")),(("reliance_gsm"),("Reliance GSM")),
                                           (("reliance_cdma"),("Reliance CDMA")),(("vodafone"),("Vodafone")),
                                           (("tata_docomo"),("Tata Docomo")),
                                           (("idea"),("Idea")),
                                           (("mts"),("MTS")),
                                           (("uninor"),("Uninor")),
                                           (("bsnl"),("BSNL")),
                                           (("loop"),("Loop")),
                                           (("videocon"),("Videocon")),
                                           (("videocon_special"),("Videocon Special")),
                                           (("virgin_cdma"),("Virgin CDMA")),
                                           (("virgin_gsm"),("Virgin GSM")),
                                           (("virgin_gsm_special"),("Virgin GSM Special")),
                                           (("mtnl_prepaid"),("MTNL")),
                                           (("mtnl_dl_special"),("MTNL DL special")),
                                           (("mtnl_dl_topup"),("MTNL DL topup")),
                                           (("mtnl_mumbai_special"),("MTNL Mumbai special")),
                                           (("mtnl_mumbai_topup"),("MTNL Mumbai topup"))
        )
        self.amount = 10.00
