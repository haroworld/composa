
from django.forms import ModelForm, ValidationError


from .models import Posts


class ComposForm(ModelForm):

    error_messages = {
            "post_error": ("Compose word or post an image"),
        }

    class Meta:
        model = Posts
        fields = ['post_body','post_image','post_privacy']

    def clean(self):
        data = self.cleaned_data
        if data.get('post_body', None) or (data.get('post_image', None)):
            return data
        else:
            raise ValidationError(
                self.error_messages['post_error'],
                code='post_error'
                )

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_body'].widget.attrs.update({'placeholder': 'Whats on your mind', 'rows':2})
        self.fields['post_body'].label = ""
        self.fields['post_body'].widget.attrs.update({'class':'mb-5 p-5 w-full focus:outline-none focus:none border-none no-resize'})
        self.fields['post_image'].widget.attrs.update({'class':'hidden'})
        self.fields['post_image'].widget.attrs.update({'id':'post_image'})
        self.fields['post_privacy'].widget.attrs.update({'class':'rounded-full border-lightBlue border-solid border-2 px-2 focus:outline-none focus:border-lightBlue'})



class CommentForm(ModelForm):
    error_messages = {
            "post_error": ("Enter comment"),
        }

    class Meta:
        model = Posts
        fields = ['post_body','post_image']



    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_body'].widget.attrs.update({'placeholder': 'Enter Comment', 'rows':1})
        #self.fields['post_body'].widget.attrs['required'] = 'required'
        self.fields['post_body'].label = ""
        self.fields['post_body'].widget.attrs.update({'class':'p-3 text-xs md:text-sm w-full focus:outline-none no-resize'})
        self.fields['post_image'].widget.attrs.update({'class':'hidden'})
        self.fields['post_image'].widget.attrs.update({'id':'com_image'})



    


class RePostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['post_body','post_image']

    # def clean(self):
    #     data = self.cleaned_data
    #     if data.get('post_body', None) or (data.get('post_image', None)):
    #         return data
    #     else:
    #         raise ValidationError(
    #             self.error_messages['post_error'],
    #             code='post_error'
    #             )

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_body'].widget.attrs.update({'placeholder': 'Add Review or Just Repost', 'rows':5})
        self.fields['post_body'].label = ""
        self.fields['post_body'].widget.attrs.update({'class':'border-none w-full focus:outline-none focus:border-none no-resize'})
        self.fields['post_image'].widget.attrs.update({'class':'hidden'})
        self.fields['post_image'].widget.attrs.update({'id':'repost_image'})


