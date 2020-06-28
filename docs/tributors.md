# The Tributors File

You can save a single metadata file in your repository that includes common fields
to use to update other metadata files. As an example, here we see a file generated
after an intial run - we index by the GitHub username since on GitHub that is our
"unit of truth." These are a few entries for Singularity Registry Server:

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessasaurus",
        "bio": "I'm the Vanessasaurus!",
        "blog": "https://vsoch.github.io"
    },
    "tschoonj": {
        "name": "Tom Schoonjans",
        "bio": "I'm a research software engineer working @rosalindfranklininstitute, and am passionate about developing quality open source software.",
        "blog": "tschoonj.github.io"
    },
    "Aneoshun": {
        "name": "Antoine Cully",
        "blog": "antoinecully.com"
    },
    "yarikoptic": {
        "name": "Yaroslav Halchenko",
        "email": "debian@onerussian.com",
        "bio": "Cheers!",
        "blog": "www.onerussian.com"
    },
    "victorsndvg": {
        "name": "victorsndvg",
        "email": "victorsv@gmail.com",
        "bio": "Scientific software engineer",
        "blog": "http://sourceforge.net/u/victorsndvg/profile/"
    },
    "RonaldEnsing": {
        "name": "Ronald Ensing"
    }
}
```

You'll notice that we only save fields that we can find (e.g., if no email is
exposed, it won't be defined. At this point we might want to update metadata
to our liking - any particular subfield for a user won't be overwritten if it's
already defined.

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessa",
        "bio": "Research Software Engineer at Stanford University",
        "blog": "https://vsoch.github.io"
    },
    "tschoonj": {
        "name": "Tom Schoonjans",
        "bio": "I'm a research software engineer working @rosalindfranklininstitute, and am passionate about developing quality open source software.",
        "blog": "tschoonj.github.io"
    },
    "Aneoshun": {
        "name": "Antoine Cully",
        "blog": "antoinecully.com"
    },
    "yarikoptic": {
        "name": "Yaroslav Halchenko",
        "email": "debian@onerussian.com",
        "bio": "Cheers!",
        "blog": "www.onerussian.com"
    },
    "victorsndvg": {
        "name": "victorsndvg",
        "email": "victorsv@gmail.com",
        "bio": "Scientific software engineer",
        "blog": "http://sourceforge.net/u/victorsndvg/profile/"
    },
    "RonaldEnsing": {
        "name": "Ronald Ensing"
    }
}
```

You can also add missing information, for example, affiliations or orcid identifiers.

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessa",
        "bio": "I'm the Vanessasaurus!",
        "affiliation": "Research Software Engineer at Stanford University",
        "blog": "https://vsoch.github.io"
    }
}
```

The following fields are known to a `.tributors` file

 - **name**: the name of the contributor
 - **email**: the email of the contributor
 - **bio**: a short bio for the contributor
 - **affiliation**: institution or other affiliation (usually comes from Orcid)
 - **blog**: a website or blog address
 - **orcid**: the orcid identifier for the contributor

For example, you might generate this file automatically to start, update
it in a text editor, and then easily update all of your other contributor files. Neat!
