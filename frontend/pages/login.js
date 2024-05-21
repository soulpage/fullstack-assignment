import LoginForm from "../components/auth/LoginForm";
import styles from "../styles/auth/auth.module.css"
import {LockKeyIcon} from "../assets/SVGIcon";
import React, {useState} from "react";
import Link from "next/link";

function LoginPage() {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const disabledClassName = isSubmitting ? styles.disabled : '';

    return (
        <div className={styles.authRoot}>
            <div className={styles.loginContainer}>
                <div className={styles.formContainer}>
                    <div className={styles.formHeader}>
                        <LockKeyIcon/>
                        <h1>Login</h1>
                    </div>
                    <LoginForm isSubmitting={isSubmitting} setIsSubmitting={setIsSubmitting}/>
                    <div className={styles.formFooter}>
                        <Link href={"#"} className={disabledClassName}>Forgot credentials?</Link>
                        <Link
                            href="/register"
                            className={disabledClassName}>Create an account</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export async function getServerSideProps(context) {
    const currUser = context.req.cookies.user || null;

    if (currUser) {
        return {
            redirect: {
                destination: '/',
                permanent: false,
            },
        }
    }

    return {
        props: {}
    }
}

export default LoginPage;
